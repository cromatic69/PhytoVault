from flask import Blueprint, request, jsonify

from services.plant_service import get_all_plants

search = Blueprint("search", __name__)


@search.route("/api/search")
def search_plants():

    keyword = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip().lower()
    family = request.args.get("family", "").strip().lower()
    sort = request.args.get("sort", "").strip().lower()

    plants = get_all_plants()

    if keyword != "":

        filtered = []

        for plant in plants:

            searchable = " ".join([

                str(plant.get("commonName", "")),
                str(plant.get("scientificName", "")),
                str(plant.get("family", "")),
                str(plant.get("part", "")),
                str(plant.get("compound", "")),
                str(plant.get("medicinalUses", ""))

            ]).lower()

            if keyword in searchable:

                filtered.append(plant)

        plants = filtered

    if category != "":

        plants = [
            p for p in plants
            if str(p.get("category", "")).strip().lower() == category
        ]

    if family != "":

        plants = [
            p for p in plants
            if str(p.get("family", "")).strip().lower() == family
        ]

    if sort == "sort a-z":

        plants = sorted(plants, key=lambda p: str(p.get("commonName", "")).lower())

    elif sort == "sort z-a":

        plants = sorted(plants, key=lambda p: str(p.get("commonName", "")).lower(), reverse=True)

    elif sort == "newest":

        plants = sorted(plants, key=lambda p: p.get("id", 0), reverse=True)

    elif sort == "oldest":

        plants = sorted(plants, key=lambda p: p.get("id", 0))

    return jsonify(plants)