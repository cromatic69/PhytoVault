"""
Research-level plant data: parsing the multi-step admin form and saving
it to the related tables. Uses the same raw mysql-connector cursor style
as the rest of the project (cursor must be created with dictionary=True).
"""

TIERS = ("A", "B", "C", "R")

ADMET_FIELDS = ("absorption", "distribution", "metabolism", "excretion", "toxicity")


def _rows(form, *names):
    """Zip parallel form lists (name[]) into dicts, dropping fully blank rows."""

    lists = [form.getlist(n + "[]") for n in names]
    count = max((len(l) for l in lists), default=0)
    rows = []

    for i in range(count):
        row = {
            n: (l[i].strip() if i < len(l) else "")
            for n, l in zip(names, lists)
        }
        if any(row.values()):
            rows.append(row)

    return rows


def parse_research_form(form):

    uses = [
        r for r in _rows(form, "use_disease", "use_part", "use_prep")
        if r["use_disease"]
    ]

    chems, seen = [], set()
    for r in _rows(form, "chem_name", "chem_class"):
        key = r["chem_name"].lower()
        if r["chem_name"] and key not in seen:
            seen.add(key)
            chems.append(r)

    bios, seen = [], set()
    for r in _rows(form, "bio_name"):
        key = r["bio_name"].lower()
        if r["bio_name"] and key not in seen:
            seen.add(key)
            bios.append(r["bio_name"][:150])

    refs = [
        r for r in _rows(
            form, "ref_authors", "ref_title", "ref_journal",
            "ref_year", "ref_doi", "ref_url"
        )
        if r["ref_title"]
    ]

    admet = {f: form.get("admet_" + f, "").strip() or None for f in ADMET_FIELDS}

    return {"uses": uses, "chems": chems, "bios": bios, "refs": refs, "admet": admet}


def _year(value):
    try:
        year = int(value)
    except (TypeError, ValueError):
        return None
    return year if 1901 <= year <= 2155 else None


def save_research_details(cursor, plant_id, data, parse_parts_text, parse_parts):
    """
    Replace the plant's medicinal uses, phytochemicals, bioactivities, ADMET
    and references with the submitted data. Concentration / plant-part
    values already stored on plant_phytochemicals are preserved.
    """

    # ---------- medicinal uses ----------
    cursor.execute("DELETE FROM plant_uses WHERE plant_id=%s", (plant_id,))

    for u in data["uses"]:

        cursor.execute(
            "SELECT use_id FROM medicinal_uses WHERE disease_name=%s LIMIT 1",
            (u["use_disease"][:200],)
        )
        row = cursor.fetchone()

        if row:
            use_id = row["use_id"]
        else:
            cursor.execute(
                "INSERT INTO medicinal_uses (disease_name) VALUES (%s)",
                (u["use_disease"][:200],)
            )
            use_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO plant_uses (plant_id, use_id, plant_part, preparation, evidence_level) "
            "VALUES (%s,%s,%s,%s,'Traditional')",
            (plant_id, use_id, u["use_part"][:150] or None, u["use_prep"] or None)
        )

    # ---------- plant parts (summary text + parts named in uses) ----------
    wanted = {name.lower(): (name, desc) for name, desc in parse_parts(parse_parts_text)}

    for u in data["uses"]:
        part = u["use_part"][:100]
        if part and part.lower() not in wanted:
            wanted[part.lower()] = (part, None)

    cursor.execute("DELETE FROM plant_parts WHERE plant_id=%s", (plant_id,))

    for name, desc in wanted.values():
        cursor.execute(
            "INSERT INTO plant_parts (plant_id, part_name, description) VALUES (%s,%s,%s)",
            (plant_id, name, desc)
        )

    # ---------- phytochemicals ----------
    cursor.execute(
        "SELECT phytochemical_id, plant_part, concentration, notes "
        "FROM plant_phytochemicals WHERE plant_id=%s", (plant_id,)
    )
    kept = {r["phytochemical_id"]: r for r in cursor.fetchall()}

    cursor.execute("DELETE FROM plant_phytochemicals WHERE plant_id=%s", (plant_id,))

    for c in data["chems"]:

        cursor.execute(
            "SELECT phytochemical_id FROM phytochemicals WHERE compound_name=%s LIMIT 1",
            (c["chem_name"][:200],)
        )
        row = cursor.fetchone()

        if row:
            chem_id = row["phytochemical_id"]
            if c["chem_class"]:
                cursor.execute(
                    "UPDATE phytochemicals SET compound_class=%s WHERE phytochemical_id=%s",
                    (c["chem_class"][:150], chem_id)
                )
        else:
            cursor.execute(
                "INSERT INTO phytochemicals (compound_name, compound_class) VALUES (%s,%s)",
                (c["chem_name"][:200], c["chem_class"][:150] or None)
            )
            chem_id = cursor.lastrowid

        old = kept.get(chem_id, {})

        cursor.execute(
            "INSERT INTO plant_phytochemicals "
            "(plant_id, phytochemical_id, plant_part, concentration, notes) "
            "VALUES (%s,%s,%s,%s,%s)",
            (plant_id, chem_id, old.get("plant_part"),
             old.get("concentration"), old.get("notes"))
        )

    # ---------- bioactivity ----------
    cursor.execute("DELETE FROM plant_bioactivities WHERE plant_id=%s", (plant_id,))

    for name in data["bios"]:
        cursor.execute(
            "INSERT INTO plant_bioactivities (plant_id, activity_name) VALUES (%s,%s)",
            (plant_id, name)
        )

    # ---------- ADMET (one row) ----------
    cursor.execute("DELETE FROM plant_admet WHERE plant_id=%s", (plant_id,))

    if any(data["admet"].values()):
        cursor.execute(
            "INSERT INTO plant_admet "
            "(plant_id, absorption, distribution, metabolism, excretion, toxicity) "
            "VALUES (%s,%s,%s,%s,%s,%s)",
            (plant_id,) + tuple(data["admet"][f] for f in ADMET_FIELDS)
        )

    # ---------- references (research_papers + paper_plants) ----------
    cursor.execute("DELETE FROM paper_plants WHERE plant_id=%s", (plant_id,))

    for r in data["refs"]:

        doi = r["ref_doi"][:255] or None
        year = _year(r["ref_year"])
        paper_id = None

        if doi:
            cursor.execute(
                "SELECT paper_id FROM research_papers WHERE doi=%s LIMIT 1", (doi,)
            )
            row = cursor.fetchone()
            paper_id = row["paper_id"] if row else None

        if paper_id is None:
            cursor.execute(
                "INSERT INTO research_papers "
                "(title, authors, journal, publication_year, doi, paper_url) "
                "VALUES (%s,%s,%s,%s,%s,%s)",
                (r["ref_title"][:500], r["ref_authors"] or None,
                 r["ref_journal"][:255] or None, year, doi, r["ref_url"] or None)
            )
            paper_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO paper_plants (paper_id, plant_id) VALUES (%s,%s)",
            (paper_id, plant_id)
        )

    # papers no longer linked to any plant or phytochemical
    cursor.execute(
        "DELETE FROM research_papers WHERE paper_id NOT IN (SELECT paper_id FROM paper_plants) "
        "AND paper_id NOT IN (SELECT paper_id FROM paper_phytochemicals)"
    )
