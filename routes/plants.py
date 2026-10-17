from flask import Blueprint, jsonify, render_template, request

from services.plant_service import (
    get_all_plants,
    get_plant_by_id
)
from services.phytochemical_service import (
    get_phytochemical_by_id,
    get_plants_by_phytochemical
)

plants = Blueprint("plants", __name__)


@plants.route("/database")
def database():

    keyword = request.args.get("search", "").lower()

    plants_data = get_all_plants()

    if keyword != "":

        filtered = []

        for plant in plants_data:

            text = " ".join([

                str(plant.get("commonName","")),
                str(plant.get("scientificName","")),
                str(plant.get("family","")),
                str(plant.get("compound","")),
                str(plant.get("part","")),
                str(plant.get("medicinalUses",""))

            ]).lower()

            if keyword in text:

                filtered.append(plant)

        plants_data = filtered

    return render_template(

        "database.html",

        plants=plants_data

    )


@plants.route("/plant/<int:plant_id>")
def plant_details(plant_id):

    plant = get_plant_by_id(plant_id)

    if not plant:

        return "Plant Not Found",404

    return render_template(

        "plant_details.html",

        plant=plant

    )


@plants.route("/api/plants")
def api_plants():

    return jsonify(

        get_all_plants()

    )


@plants.route("/phytochemical/<int:phytochemical_id>")
def phytochemical_details(phytochemical_id):

    phytochemical = get_phytochemical_by_id(phytochemical_id)

    if not phytochemical:

        return "Phytochemical Not Found", 404

    return render_template(

        "phytochemical_details.html",

        phytochemical=phytochemical,

        plants=get_plants_by_phytochemical(phytochemical_id)

    )