from utils.db import get_db


def get_phytochemical_by_id(phytochemical_id):

    connection = get_db()

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM phytochemicals WHERE phytochemical_id=%s",
        (phytochemical_id,)
    )

    phytochemical = cursor.fetchone()

    cursor.close()

    connection.close()

    return phytochemical


def get_plants_by_phytochemical(phytochemical_id):

    connection = get_db()

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            p.plant_id,
            p.common_name,
            p.scientific_name,
            p.family,
            p.image_path,
            pcp.plant_part,
            pcp.concentration
        FROM plant_phytochemicals pcp
        JOIN plants p
            ON p.plant_id = pcp.plant_id
        WHERE pcp.phytochemical_id=%s
        ORDER BY p.common_name
        """,
        (phytochemical_id,)
    )

    plants = cursor.fetchall()

    cursor.close()

    connection.close()

    return plants
