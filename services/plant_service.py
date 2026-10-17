from utils.db import get_db


def get_all_plants():

    connection = get_db()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""

        SELECT

            p.plant_id AS id,
            p.common_name AS commonName,
            p.scientific_name AS scientificName,
            p.family,
            p.category,
            p.image_path,

            GROUP_CONCAT(
                DISTINCT pp.part_name
                SEPARATOR ', '
            ) AS part,

            GROUP_CONCAT(
                DISTINCT ph.compound_name
                SEPARATOR ', '
            ) AS compound,

            GROUP_CONCAT(
                DISTINCT mu.disease_name
                SEPARATOR ', '
            ) AS medicinalUses

        FROM plants p

        LEFT JOIN plant_parts pp
            ON pp.plant_id = p.plant_id

        LEFT JOIN plant_phytochemicals ppc
            ON ppc.plant_id = p.plant_id

        LEFT JOIN phytochemicals ph
            ON ph.phytochemical_id = ppc.phytochemical_id

        LEFT JOIN plant_uses pu
            ON pu.plant_id = p.plant_id

        LEFT JOIN medicinal_uses mu
            ON mu.use_id = pu.use_id

        GROUP BY p.plant_id

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
        SELECT mu.disease_name, pu.evidence_level, pu.notes
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

    cursor.close()

    connection.close()

    return plant