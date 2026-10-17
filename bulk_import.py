"""
PhytoVault bulk importer.

Reads phytovault_data_template.xlsx (filled in) and inserts rows into:
  plants, phytochemicals, medicinal_uses, plant_parts,
  plant_phytochemicals (link table), plant_uses (link table)

Usage:
    python bulk_import.py path/to/filled_template.xlsx           # dry run (default)
    python bulk_import.py path/to/filled_template.xlsx --commit  # actually writes to the DB

Run this from the PhytoVault project root (so it can import config.py / mysql.connector),
or place it in the project folder alongside app.py.
"""

import sys
import openpyxl
import mysql.connector

# --- DB connection -----------------------------------------------------
# Adjust these to match config.py, or better: import Config from the project
# once the credentials have been moved to environment variables.
from config import Config


def get_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
    )


EVIDENCE_LEVELS = {"traditional", "experimental", "clinical"}
PLANT_PARTS = {
    "leaf", "root", "stem", "flower", "fruit", "seed", "bark", "rhizome", "whole plant"
}


def is_blank_row(row):
    return all(v is None or str(v).strip() == "" for v in row)


def read_sheet(wb, name):
    """Yields dict rows keyed by header, skipping the example row (yellow-filled) and blanks."""
    if name not in wb.sheetnames:
        return
    ws = wb[name]
    headers = [str(c.value).strip() if c.value else "" for c in ws[1]]
    for i, row in enumerate(ws.iter_rows(min_row=2, values_only=False), start=2):
        values = [c.value for c in row]
        if is_blank_row(values):
            continue
        # Skip the pre-filled example row (pale yellow fill, tag FFF2CC)
        first_cell = row[0]
        if first_cell.fill and first_cell.fill.fgColor and first_cell.fill.fgColor.rgb == "00FFF2CC":
            continue
        yield i, dict(zip(headers, values))


def clean(v):
    if v is None:
        return None
    if isinstance(v, str):
        v = v.strip()
        return v if v else None
    return v


def yn_to_bool(v):
    if v is None:
        return None
    return str(v).strip().lower() in ("yes", "y", "true", "1")


def main():
    if len(sys.argv) < 2:
        print("Usage: python bulk_import.py <template.xlsx> [--commit]")
        sys.exit(1)

    path = sys.argv[1]
    commit = "--commit" in sys.argv[2:]

    wb = openpyxl.load_workbook(path, data_only=True)

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    stats = {
        "plants": 0, "phytochemicals": 0, "medicinal_uses": 0,
        "plant_parts": 0, "plant_phytochemical_links": 0, "plant_use_links": 0,
        "skipped": [],
    }

    # Caches so we don't re-query the same lookup repeatedly
    plant_id_by_name = {}
    compound_id_by_name = {}
    disease_id_by_name = {}

    def get_or_create_plant_id(common_name):
        if common_name in plant_id_by_name:
            return plant_id_by_name[common_name]
        cur.execute("SELECT plant_id FROM plants WHERE common_name=%s", (common_name,))
        row = cur.fetchone()
        if row:
            plant_id_by_name[common_name] = row["plant_id"]
            return row["plant_id"]
        return None

    def get_or_create_compound_id(compound_name, extra=None):
        if compound_name in compound_id_by_name:
            return compound_id_by_name[compound_name]
        cur.execute(
            "SELECT phytochemical_id FROM phytochemicals WHERE compound_name=%s",
            (compound_name,),
        )
        row = cur.fetchone()
        if row:
            compound_id_by_name[compound_name] = row["phytochemical_id"]
            return row["phytochemical_id"]
        if extra is None:
            return None  # caller must create it first via the Phytochemicals sheet
        cur.execute(
            """INSERT INTO phytochemicals
               (compound_name, molecular_formula, molecular_weight, smiles,
                iupac_name, pubchem_cid, description, biological_activity)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            extra,
        )
        new_id = cur.lastrowid
        compound_id_by_name[compound_name] = new_id
        return new_id

    def get_or_create_disease_id(disease_name, description=None):
        if disease_name in disease_id_by_name:
            return disease_id_by_name[disease_name]
        cur.execute("SELECT use_id FROM medicinal_uses WHERE disease_name=%s", (disease_name,))
        row = cur.fetchone()
        if row:
            disease_id_by_name[disease_name] = row["use_id"]
            return row["use_id"]
        cur.execute(
            "INSERT INTO medicinal_uses (disease_name, description) VALUES (%s,%s)",
            (disease_name, description),
        )
        new_id = cur.lastrowid
        disease_id_by_name[disease_name] = new_id
        return new_id

    # ---------------- Plants ----------------
    for rownum, r in read_sheet(wb, "Plants"):
        common_name = clean(r.get("common_name*"))
        scientific_name = clean(r.get("scientific_name*"))
        if not common_name or not scientific_name:
            stats["skipped"].append(f"Plants row {rownum}: missing common_name or scientific_name")
            continue

        cur.execute("SELECT plant_id FROM plants WHERE common_name=%s", (common_name,))
        existing = cur.fetchone()
        image_filename = clean(r.get("image_filename"))
        image_path = f"images/plants/{image_filename}" if image_filename else None

        if existing:
            plant_id_by_name[common_name] = existing["plant_id"]
        else:
            cur.execute(
                """INSERT INTO plants
                   (common_name, scientific_name, family, genus, species, category,
                    habitat, origin, description, traditional_uses,
                    conservation_status, toxicity, edible, medicinal, image_path)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    common_name, scientific_name, clean(r.get("family")),
                    clean(r.get("genus")), clean(r.get("species")), clean(r.get("category")),
                    clean(r.get("habitat")), clean(r.get("origin")),
                    clean(r.get("description")), clean(r.get("traditional_uses")),
                    clean(r.get("conservation_status")), clean(r.get("toxicity")),
                    yn_to_bool(r.get("edible (yes/no)")), yn_to_bool(r.get("medicinal (yes/no)")),
                    image_path,
                ),
            )
            plant_id_by_name[common_name] = cur.lastrowid
            stats["plants"] += 1

    # ---------------- Phytochemicals ----------------
    for rownum, r in read_sheet(wb, "Phytochemicals"):
        compound_name = clean(r.get("compound_name*"))
        if not compound_name:
            stats["skipped"].append(f"Phytochemicals row {rownum}: missing compound_name")
            continue
        cur.execute(
            "SELECT phytochemical_id FROM phytochemicals WHERE compound_name=%s",
            (compound_name,),
        )
        existing = cur.fetchone()
        if existing:
            compound_id_by_name[compound_name] = existing["phytochemical_id"]
            continue
        cur.execute(
            """INSERT INTO phytochemicals
               (compound_name, molecular_formula, molecular_weight, smiles,
                iupac_name, pubchem_cid, description, biological_activity)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (
                compound_name, clean(r.get("molecular_formula")),
                clean(r.get("molecular_weight")), clean(r.get("smiles")),
                clean(r.get("iupac_name")), clean(r.get("pubchem_cid")),
                clean(r.get("description")), clean(r.get("biological_activity")),
            ),
        )
        compound_id_by_name[compound_name] = cur.lastrowid
        stats["phytochemicals"] += 1

    # ---------------- Medicinal Uses ----------------
    for rownum, r in read_sheet(wb, "Medicinal_Uses"):
        disease_name = clean(r.get("disease_name*"))
        if not disease_name:
            stats["skipped"].append(f"Medicinal_Uses row {rownum}: missing disease_name")
            continue
        cur.execute("SELECT use_id FROM medicinal_uses WHERE disease_name=%s", (disease_name,))
        existing = cur.fetchone()
        if existing:
            disease_id_by_name[disease_name] = existing["use_id"]
            continue
        cur.execute(
            "INSERT INTO medicinal_uses (disease_name, description) VALUES (%s,%s)",
            (disease_name, clean(r.get("description"))),
        )
        disease_id_by_name[disease_name] = cur.lastrowid
        stats["medicinal_uses"] += 1

    # ---------------- Plant Parts ----------------
    part_col = "part_name (Leaf/Root/Stem/Flower/Fruit/Seed/Bark/Rhizome/Whole Plant)"
    for rownum, r in read_sheet(wb, "Plant_Parts"):
        plant_name = clean(r.get("plant_common_name*"))
        part_name = clean(r.get(part_col))
        if not plant_name or not part_name:
            stats["skipped"].append(f"Plant_Parts row {rownum}: missing plant or part name")
            continue
        if part_name.lower() not in PLANT_PARTS:
            stats["skipped"].append(
                f"Plant_Parts row {rownum}: '{part_name}' isn't a valid part "
                f"(must be one of {sorted(PLANT_PARTS)})"
            )
            continue
        plant_id = get_or_create_plant_id(plant_name)
        if plant_id is None:
            stats["skipped"].append(f"Plant_Parts row {rownum}: plant '{plant_name}' not found — add it to Plants sheet first")
            continue
        cur.execute(
            "INSERT INTO plant_parts (plant_id, part_name, description) VALUES (%s,%s,%s)",
            (plant_id, part_name.title(), clean(r.get("description"))),
        )
        stats["plant_parts"] += 1

    # ---------------- Plant <-> Phytochemical links ----------------
    for rownum, r in read_sheet(wb, "Plant_Phytochemical_Links"):
        plant_name = clean(r.get("plant_common_name*"))
        compound_name = clean(r.get("compound_name*"))
        if not plant_name or not compound_name:
            stats["skipped"].append(f"Plant_Phytochemical_Links row {rownum}: missing plant or compound name")
            continue
        plant_id = get_or_create_plant_id(plant_name)
        compound_id = get_or_create_compound_id(compound_name)
        if plant_id is None:
            stats["skipped"].append(f"Plant_Phytochemical_Links row {rownum}: plant '{plant_name}' not found")
            continue
        if compound_id is None:
            stats["skipped"].append(f"Plant_Phytochemical_Links row {rownum}: compound '{compound_name}' not found — add it to Phytochemicals sheet first")
            continue
        cur.execute(
            """INSERT INTO plant_phytochemicals
               (plant_id, phytochemical_id, plant_part, concentration, notes)
               VALUES (%s,%s,%s,%s,%s)""",
            (plant_id, compound_id, clean(r.get("plant_part")),
             clean(r.get("concentration")), clean(r.get("notes"))),
        )
        stats["plant_phytochemical_links"] += 1

    # ---------------- Plant <-> Use links ----------------
    evidence_col = "evidence_level (Traditional/Experimental/Clinical)"
    for rownum, r in read_sheet(wb, "Plant_Use_Links"):
        plant_name = clean(r.get("plant_common_name*"))
        disease_name = clean(r.get("disease_name*"))
        if not plant_name or not disease_name:
            stats["skipped"].append(f"Plant_Use_Links row {rownum}: missing plant or disease name")
            continue
        plant_id = get_or_create_plant_id(plant_name)
        disease_id = get_or_create_disease_id(disease_name)
        if plant_id is None:
            stats["skipped"].append(f"Plant_Use_Links row {rownum}: plant '{plant_name}' not found")
            continue
        evidence = clean(r.get(evidence_col)) or "Traditional"
        if evidence.lower() not in EVIDENCE_LEVELS:
            evidence = "Traditional"
        cur.execute(
            """INSERT INTO plant_uses (plant_id, use_id, evidence_level, notes)
               VALUES (%s,%s,%s,%s)""",
            (plant_id, disease_id, evidence.title(), clean(r.get("notes"))),
        )
        stats["plant_use_links"] += 1

    if commit:
        conn.commit()
        print("✅ Committed to the database.")
    else:
        conn.rollback()
        print("🔎 Dry run only — nothing was written. Re-run with --commit to apply.")

    cur.close()
    conn.close()

    print("\n--- Summary ---")
    for k, v in stats.items():
        if k != "skipped":
            print(f"{k}: {v}")
    if stats["skipped"]:
        print(f"\n⚠️  {len(stats['skipped'])} row(s) skipped:")
        for s in stats["skipped"]:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
