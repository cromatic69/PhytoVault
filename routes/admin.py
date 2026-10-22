from flask import Blueprint, render_template, request, redirect, flash, session
from werkzeug.utils import secure_filename
from utils.db import get_db
from services.research_service import (
    parse_research_form,
    save_research_details,
    TIERS
)
import os
import re

admin = Blueprint("admin", __name__)

UPLOAD_FOLDER = "static/images/plants"


os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@admin.before_request
def protect_admin():

    user = session.get("user")
    if not user:
        return redirect("/login")
    if user["role"] != "Admin":
            return redirect("/")


@admin.route("/admin")
def dashboard():

    connection = get_db()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""

        SELECT *

        FROM plants

        ORDER BY common_name

    """)

    plants = cursor.fetchall()

    cursor.close()

    connection.close()

    return render_template(

        "admin.html",

        plants=plants

    )


def split_list(value):

    """Split a comma / semicolon / newline separated string into unique, trimmed items."""

    items = []

    for item in re.split(r"[,;\n]+", value or ""):

        item = item.strip()

        if item and item.lower() not in [i.lower() for i in items]:

            items.append(item)

    return items


def parse_parts(value):

    """One part per line / semicolon. 'Part: description' -> (name, description)."""

    parts = []
    seen = set()

    for entry in re.split(r"[;\n]+", value or ""):

        entry = entry.strip()

        if not entry:
            continue

        if ":" in entry:
            name, desc = entry.split(":", 1)
        else:
            name, desc = entry, ""

        name = name.strip()[:100]

        if not name or name.lower() in seen:
            continue

        seen.add(name.lower())

        parts.append((name, desc.strip() or None))

    return parts


def save_image(default_path):

    """Save an uploaded image (if any) and return the path to store."""

    image = request.files.get("image")

    if image and image.filename != "":

        filename = secure_filename(image.filename)

        image.save(os.path.join(UPLOAD_FOLDER, filename))

        return "images/plants/" + filename

    return default_path


def sync_plant_details(cursor, plant_id, parts, uses, chems):

    """
    Make the plant's parts, medicinal uses and phytochemicals match the
    submitted lists. Entries that are still present are left untouched
    (so evidence levels, concentrations, etc. are kept); removed ones are
    deleted and new ones are added.
    """

    # ----- plant parts -----
    cursor.execute(
        "SELECT part_name FROM plant_parts WHERE plant_id=%s",
        (plant_id,)
    )

    existing_parts = {r["part_name"].lower() for r in cursor.fetchall()}

    wanted_parts = {name.lower() for name, _ in parts}

    for name in existing_parts - wanted_parts:

        cursor.execute(
            "DELETE FROM plant_parts WHERE plant_id=%s AND part_name=%s",
            (plant_id, name)
        )

    for name, desc in parts:

        if name.lower() in existing_parts:

            cursor.execute(
                "UPDATE plant_parts SET description=%s WHERE plant_id=%s AND part_name=%s",
                (desc, plant_id, name)
            )

        else:

            cursor.execute(
                "INSERT INTO plant_parts (plant_id, part_name, description) VALUES (%s,%s,%s)",
                (plant_id, name, desc)
            )

    # ----- medicinal uses -----
    cursor.execute("""
        SELECT pu.use_id, mu.disease_name
        FROM plant_uses pu
        JOIN medicinal_uses mu ON mu.use_id = pu.use_id
        WHERE pu.plant_id=%s
    """, (plant_id,))

    existing_uses = {r["disease_name"].lower(): r["use_id"] for r in cursor.fetchall()}

    wanted_uses = {u.lower() for u in uses}

    for name, use_id in existing_uses.items():

        if name not in wanted_uses:

            cursor.execute(
                "DELETE FROM plant_uses WHERE plant_id=%s AND use_id=%s",
                (plant_id, use_id)
            )

    for disease in uses:

        if disease.lower() in existing_uses:
            continue

        cursor.execute(
            "SELECT use_id FROM medicinal_uses WHERE disease_name=%s",
            (disease,)
        )

        row = cursor.fetchone()

        if row:
            use_id = row["use_id"]
        else:
            cursor.execute(
                "INSERT INTO medicinal_uses (disease_name, description) VALUES (%s,%s)",
                (disease, None)
            )
            use_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO plant_uses (plant_id, use_id, evidence_level, notes) VALUES (%s,%s,%s,%s)",
            (plant_id, use_id, "Traditional", None)
        )

    # ----- phytochemicals -----
    cursor.execute("""
        SELECT DISTINCT ppc.phytochemical_id, ph.compound_name
        FROM plant_phytochemicals ppc
        JOIN phytochemicals ph ON ph.phytochemical_id = ppc.phytochemical_id
        WHERE ppc.plant_id=%s
    """, (plant_id,))

    existing_chems = {r["compound_name"].lower(): r["phytochemical_id"] for r in cursor.fetchall()}

    wanted_chems = {c.lower() for c in chems}

    for name, chem_id in existing_chems.items():

        if name not in wanted_chems:

            cursor.execute(
                "DELETE FROM plant_phytochemicals WHERE plant_id=%s AND phytochemical_id=%s",
                (plant_id, chem_id)
            )

    for compound in chems:

        if compound.lower() in existing_chems:
            continue

        cursor.execute(
            "SELECT phytochemical_id FROM phytochemicals WHERE compound_name=%s",
            (compound,)
        )

        row = cursor.fetchone()

        if row:
            chem_id = row["phytochemical_id"]
        else:
            cursor.execute(
                "INSERT INTO phytochemicals (compound_name) VALUES (%s)",
                (compound,)
            )
            chem_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO plant_phytochemicals (plant_id, phytochemical_id, plant_part, concentration, notes) VALUES (%s,%s,%s,%s,%s)",
            (plant_id, chem_id, None, None, None)
        )


PLANT_FIELDS = (
    "common_name", "scientific_name", "family", "genus", "species",
    "kingdom", "phylum", "class_name", "order_name", "occurrence_tier",
    "category", "origin", "distribution", "habitat", "description",
    "traditional_uses", "conservation_status", "toxicity"
)


def form_values():

    values = []

    for f in PLANT_FIELDS:

        value = request.form.get(f, "").strip()

        if f == "occurrence_tier":
            value = value.upper() if value.upper() in TIERS else None

        values.append(value)

    return values


def save_all_details(cursor, plant_id):

    save_research_details(
        cursor, plant_id,
        parse_research_form(request.form),
        request.form.get("plant_parts"),
        parse_parts
    )


def empty_research():

    return {"uses": [], "chems": [], "bios": [], "admet": {}, "refs": []}


def load_research(cursor, plant_id):
    """Existing structured data for pre-filling the edit wizard."""

    cursor.execute("""
        SELECT mu.disease_name, pu.plant_part, pu.preparation
        FROM plant_uses pu
        JOIN medicinal_uses mu ON mu.use_id = pu.use_id
        WHERE pu.plant_id=%s
        ORDER BY pu.id
    """, (plant_id,))
    uses = cursor.fetchall()

    cursor.execute("""
        SELECT ph.compound_name, ph.compound_class
        FROM plant_phytochemicals ppc
        JOIN phytochemicals ph ON ph.phytochemical_id = ppc.phytochemical_id
        WHERE ppc.plant_id=%s
        GROUP BY ph.phytochemical_id, ph.compound_name, ph.compound_class
        ORDER BY MIN(ppc.id)
    """, (plant_id,))
    chems = cursor.fetchall()

    cursor.execute(
        "SELECT activity_name FROM plant_bioactivities WHERE plant_id=%s ORDER BY bioactivity_id",
        (plant_id,)
    )
    bios = [r["activity_name"] for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM plant_admet WHERE plant_id=%s", (plant_id,))
    admet = cursor.fetchone() or {}

    cursor.execute("""
        SELECT rp.authors, rp.title, rp.journal, rp.publication_year AS year,
               rp.doi, rp.paper_url AS url
        FROM paper_plants pp
        JOIN research_papers rp ON rp.paper_id = pp.paper_id
        WHERE pp.plant_id=%s
        ORDER BY pp.id
    """, (plant_id,))
    refs = cursor.fetchall()

    return {"uses": uses, "chems": chems, "bios": bios, "admet": admet, "refs": refs}


@admin.route("/admin/add", methods=["GET", "POST"])
def add_plant():

    if request.method == "POST":

        image_path = save_image("images/plants/default.jpg")

        connection = get_db()

        cursor = connection.cursor(dictionary=True)

        try:

            cursor.execute(
                "INSERT INTO plants (" + ", ".join(PLANT_FIELDS) + ", image_path) VALUES ("
                + ", ".join(["%s"] * (len(PLANT_FIELDS) + 1)) + ")",
                form_values() + [image_path]
            )

            plant_id = cursor.lastrowid

            save_all_details(cursor, plant_id)

            connection.commit()

        except Exception:

            connection.rollback()

            raise

        finally:

            cursor.close()

            connection.close()

        flash("Plant Added Successfully")

        return redirect("/admin")

    return render_template(

        "add_plant.html",

        plant={},
        research=empty_research(),
        plant_parts_text=""

    )


@admin.route("/admin/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    connection = get_db()

    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        image_path = save_image(request.form.get("old_image", ""))

        try:

            cursor.execute(
                "UPDATE plants SET "
                + ", ".join(f + "=%s" for f in PLANT_FIELDS)
                + ", image_path=%s WHERE plant_id=%s",
                form_values() + [image_path, id]
            )

            save_all_details(cursor, id)

            connection.commit()

        except Exception:

            connection.rollback()

            raise

        finally:

            cursor.close()

            connection.close()

        flash("Plant Updated Successfully")

        return redirect("/admin")

    cursor.execute(
        "SELECT * FROM plants WHERE plant_id=%s",
        (id,)
    )

    plant = cursor.fetchone()

    cursor.execute(
        "SELECT part_name, description FROM plant_parts WHERE plant_id=%s ORDER BY part_name",
        (id,)
    )

    parts = cursor.fetchall()

    research = load_research(cursor, id)

    cursor.close()

    connection.close()

    plant_parts_text = "\n".join(
        p["part_name"] + (": " + p["description"] if p["description"] else "")
        for p in parts
    )

    return render_template(

        "edit_plant.html",

        plant=plant,
        research=research,
        plant_parts_text=plant_parts_text

    )


@admin.route("/admin/delete/<int:id>")
def delete(id):

    connection = get_db()

    cursor = connection.cursor()

    cursor.execute(

        "DELETE FROM plants WHERE plant_id=%s",

        (id,)

    )

    connection.commit()

    cursor.close()

    connection.close()

    flash("Plant Deleted Successfully")

    return redirect("/admin")


# -----------------------------
# Manage Admins
# -----------------------------
VALID_FALLBACK_ROLES = ("Student", "Researcher", "Faculty")


@admin.route("/admin/manage-admins")
def manage_admins():

    connection = get_db()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""

        SELECT
            user_id,
            full_name,
            username,
            email,
            role

        FROM users

        ORDER BY
            (role = 'Admin') DESC,
            full_name

    """)

    users = cursor.fetchall()

    cursor.close()

    connection.close()

    return render_template(

        "manage_admins.html",

        users=users,

        current_user=session.get("user")

    )


@admin.route("/admin/manage-admins/promote/<int:user_id>", methods=["POST"])
def promote_admin(user_id):

    connection = get_db()

    cursor = connection.cursor()

    cursor.execute(

        "UPDATE users SET role='Admin' WHERE user_id=%s",

        (user_id,)

    )

    connection.commit()

    cursor.close()

    connection.close()

    flash("User promoted to Admin.")

    return redirect("/admin/manage-admins")


@admin.route("/admin/manage-admins/demote/<int:user_id>", methods=["POST"])
def demote_admin(user_id):

    current_user = session.get("user")

    if current_user and current_user["id"] == user_id:

        flash("You can't remove your own admin access.")

        return redirect("/admin/manage-admins")

    connection = get_db()

    cursor = connection.cursor(dictionary=True)

    cursor.execute(

        "SELECT COUNT(*) AS admin_count FROM users WHERE role='Admin'"

    )

    admin_count = cursor.fetchone()["admin_count"]

    if admin_count <= 1:

        cursor.close()

        connection.close()

        flash("At least one Admin must remain - promote someone else first.")

        return redirect("/admin/manage-admins")

    fallback_role = request.form.get("fallback_role", "Student")

    if fallback_role not in VALID_FALLBACK_ROLES:

        fallback_role = "Student"

    cursor.execute(

        "UPDATE users SET role=%s WHERE user_id=%s",

        (fallback_role, user_id)

    )

    connection.commit()

    cursor.close()

    connection.close()

    flash("Admin access removed.")

    return redirect("/admin/manage-admins")