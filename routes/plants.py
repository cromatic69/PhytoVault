from flask import Blueprint, jsonify, render_template, request

from services.plant_service import (
    get_all_plants,
    get_plant_by_id
)
from services.search_service import filter_plants
from services.phytochemical_service import (
    get_phytochemical_by_id,
    get_plants_by_phytochemical
)

plants = Blueprint("plants", __name__)


@plants.route("/database")
def database():

    keyword = request.args.get("search", "")

    field = request.args.get("field", "all")

    plants_data = filter_plants(get_all_plants(), keyword, field)

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