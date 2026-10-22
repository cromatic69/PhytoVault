from utils.db import get_db


def get_all_plants():

    connection = get_db()

    cursor = connection.cursor(dictionary=True)

    # GROUP_CONCAT truncates at 1024 chars by default
    cursor.execute("SET SESSION group_concat_max_len = 1000000")

    cursor.execute("""

        SELECT

            p.plant_id AS id,
            p.common_name AS commonName,
            p.scientific_name AS scientificName,
            p.family,
            p.category,
            p.distribution,
            p.occurrence_tier AS occurrenceTier,
            p.image_path,

            (SELECT GROUP_CONCAT(DISTINCT pp.part_name SEPARATOR ', ')
               FROM plant_parts pp
              WHERE pp.plant_id = p.plant_id) AS part,

            (SELECT GROUP_CONCAT(DISTINCT ph.compound_name SEPARATOR ', ')
               FROM plant_phytochemicals ppc
               JOIN phytochemicals ph
                 ON ph.phytochemical_id = ppc.phytochemical_id
              WHERE ppc.plant_id = p.plant_id) AS compound,

            (SELECT GROUP_CONCAT(DISTINCT mu.disease_name SEPARATOR ', ')
               FROM plant_uses pu
               JOIN medicinal_uses mu
                 ON mu.use_id = pu.use_id
              WHERE pu.plant_id = p.plant_id) AS medicinalUses,

            (SELECT GROUP_CONCAT(DISTINCT pb.activity_name SEPARATOR ', ')
               FROM plant_bioactivities pb
              WHERE pb.plant_id = p.plant_id) AS bioactivity

        FROM plants p

        ORDER BY p.plant_id

    """)

    plants = cursor.fetchall()

    cursor.close()

    connection.close()

    return plants


def get_plant_by_id(plant_id):

    connection = get_db()

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM plants WHERE plant_id=%s",
        (plant_id,)
    )

    plant = cursor.fetchone()

    if not plant:

        cursor.close()
        connection.close()

        return None

    cursor.execute(
        """
        SELECT part_name, description
        FROM plant_parts
        WHERE plant_id=%s
        ORDER BY part_name
        """,
        (plant_id,)
    )

    plant["parts"] = cursor.fetchall()

    cursor.execute(
        """
        SELECT
            ph.phytochemical_id,
            ph.compound_name,
            ph.compound_class,
            ph.molecular_formula,
            ph.pubchem_cid,
            pcp.plant_part,
            pcp.concentration
        FROM plant_phytochemicals pcp
        JOIN phytochemicals ph
            ON ph.phytochemical_id = pcp.phytochemical_id
        WHERE pcp.plant_id=%s
        ORDER BY ph.compound_name
        """,
        (plant_id,)
    )

    plant["phytochemicals"] = cursor.fetchall()

    cursor.execute(
        """
        SELECT mu.disease_name, pu.plant_part, pu.preparation, pu.evidence_level, pu.notes
        FROM plant_uses pu
        JOIN medicinal_uses mu
            ON mu.use_id = pu.use_id
        WHERE pu.plant_id=%s
        ORDER BY mu.disease_name
        """,
        (plant_id,)
    )

    plant["medicinal_uses"] = cursor.fetchall()

    cursor.execute(
        """
        SELECT image_path, caption
        FROM plant_images
        WHERE plant_id=%s
        """,
        (plant_id,)
    )

    plant["gallery"] = cursor.fetchall()

    cursor.execute(
        "SELECT activity_name FROM plant_bioactivities "
        "WHERE plant_id=%s ORDER BY activity_name",
        (plant_id,)
    )

    plant["bioactivities"] = [r["activity_name"] for r in cursor.fetchall()]

    cursor.execute(
        "SELECT absorption, distribution, metabolism, excretion, toxicity "
        "FROM plant_admet WHERE plant_id=%s",
        (plant_id,)
    )

    plant["admet"] = cursor.fetchone()

    cursor.execute(
        """
        SELECT rp.paper_id, rp.authors, rp.title, rp.journal,
               rp.publication_year AS year, rp.doi, rp.paper_url AS url
        FROM paper_plants pp
        JOIN research_papers rp ON rp.paper_id = pp.paper_id
        WHERE pp.plant_id=%s
        ORDER BY rp.publication_year DESC, rp.title
        """,
        (plant_id,)
    )

    plant["references"] = cursor.fetchall()

    cursor.close()

    connection.close()

    return plant