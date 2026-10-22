"""Field-aware plant search, shared by /database and /api/search."""

# search field -> keys of the get_all_plants() dicts to look in
FIELD_KEYS = {
    "common_name": ["commonName"],
    "scientific_name": ["scientificName"],
    "family": ["family"],
    "disease": ["medicinalUses"],
    "phytochemical": ["compound"],
    "bioactivity": ["bioactivity"],
    "distribution": ["distribution"],
}

ALL_KEYS = [
    "commonName", "scientificName", "family", "part", "compound",
    "medicinalUses", "bioactivity", "distribution",
]


def filter_plants(plants, keyword, field="all"):

    keyword = (keyword or "").strip().lower()

    if not keyword:
        return plants

    keys = FIELD_KEYS.get((field or "all").strip().lower(), ALL_KEYS)

    return [
        p for p in plants
        if keyword in " ".join(str(p.get(k) or "") for k in keys).lower()
    ]
