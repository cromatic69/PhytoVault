"use strict";

(function () {

    const form = document.getElementById("plantWizard");
    if (!form) return;

    const panels = Array.from(form.querySelectorAll(".wiz-panel"));
    const stepBtns = Array.from(document.querySelectorAll(".wiz-step"));
    const prev = document.getElementById("wizPrev");
    const next = document.getElementById("wizNext");
    const submit = document.getElementById("wizSubmit");
    const bar = document.getElementById("wizBar");

    let current = 0;
    const visited = new Set([0]);

    function validateStep(index) {
        let ok = true;
        panels[index].querySelectorAll("[required]").forEach(function (el) {
            const bad = !el.value.trim();
            el.classList.toggle("is-invalid", bad);
            if (bad) ok = false;
        });
        if (!ok) {
            const first = panels[index].querySelector(".is-invalid");
            if (first) first.focus();
        }
        return ok;
    }

    function show(index) {
        current = Math.max(0, Math.min(panels.length - 1, index));
        visited.add(current);

        panels.forEach(function (p, i) { p.hidden = i !== current; });

        stepBtns.forEach(function (b, i) {
            b.classList.toggle("active", i === current);
            b.classList.toggle("done", i !== current && visited.has(i));
        });

        prev.hidden = current === 0;
        next.hidden = current === panels.length - 1;
        submit.hidden = current !== panels.length - 1;
        bar.style.width = ((current + 1) / panels.length * 100) + "%";

        const mirror = document.getElementById("familyMirror");
        if (mirror) mirror.value = document.getElementById("family").value;

        window.scrollTo({ top: 0, behavior: "smooth" });
    }

    function go(index) {
        // leaving step 1 forwards requires the mandatory names
        if (index > 0 && !validateStep(0)) { show(0); return; }
        show(index);
    }

    next.addEventListener("click", function () { go(current + 1); });
    prev.addEventListener("click", function () { show(current - 1); });
    stepBtns.forEach(function (b) {
        b.addEventListener("click", function () { go(parseInt(b.dataset.step, 10)); });
    });

    // Enter inside a single-line input moves forward instead of submitting early
    form.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && e.target.tagName === "INPUT" && e.target.type !== "submit") {
            e.preventDefault();
            if (current < panels.length - 1) go(current + 1);
        }
    });

    form.addEventListener("submit", function (e) {
        if (!validateStep(0)) { e.preventDefault(); show(0); }
    });

    form.addEventListener("input", function (e) {
        if (e.target.classList.contains("is-invalid")) e.target.classList.remove("is-invalid");
    });

    // ----- dynamic rows (no page reload) -----
    function addRow(listId, tplId, values) {
        const list = document.getElementById(listId);
        const node = document.getElementById(tplId).content.firstElementChild.cloneNode(true);
        if (values) {
            node.querySelectorAll("input").forEach(function (inp, i) {
                if (values[i] !== undefined) inp.value = values[i];
            });
        }
        list.appendChild(node);
        renumberRefs();
        return node;
    }

    function renumberRefs() {
        document.querySelectorAll("#list-ref .ref-label").forEach(function (el, i) {
            el.textContent = "Reference " + (i + 1);
        });
    }

    form.addEventListener("click", function (e) {

        const add = e.target.closest(".add-row");
        if (add) {
            const row = addRow(add.dataset.target, add.dataset.tpl);
            const input = row.querySelector("input");
            if (input) input.focus();
            return;
        }

        const rm = e.target.closest(".remove-row");
        if (rm) {
            rm.closest(".repeat-row").remove();
            renumberRefs();
            return;
        }

        const quick = e.target.closest(".quick-bio");
        if (quick) {
            const name = quick.dataset.name;
            const exists = Array.from(document.querySelectorAll('[name="bio_name[]"]'))
                .some(function (i) { return i.value.trim().toLowerCase() === name.toLowerCase(); });
            if (!exists) {
                // reuse an empty row if there is one
                const empty = Array.from(document.querySelectorAll('[name="bio_name[]"]'))
                    .find(function (i) { return !i.value.trim(); });
                if (empty) empty.value = name; else addRow("list-bio", "tpl-bio", [name]);
            }
        }
    });

    const bulkBtn = document.getElementById("chemBulkBtn");
    if (bulkBtn) {
        bulkBtn.addEventListener("click", function () {
            const box = document.getElementById("chemBulk");
            const have = new Set(Array.from(document.querySelectorAll('[name="chem_name[]"]'))
                .map(function (i) { return i.value.trim().toLowerCase(); }));
            box.value.split(/[,;\n]+/).forEach(function (raw) {
                const name = raw.trim();
                if (name && !have.has(name.toLowerCase())) {
                    have.add(name.toLowerCase());
                    addRow("list-chem", "tpl-chem", [name]);
                }
            });
            box.value = "";
        });
    }

    // Start with one empty row in each list so the step is never blank
    [["list-use", "tpl-use"], ["list-chem", "tpl-chem"], ["list-bio", "tpl-bio"], ["list-ref", "tpl-ref"]]
        .forEach(function (pair) {
            const list = document.getElementById(pair[0]);
            if (list && !list.children.length) addRow(pair[0], pair[1]);
        });
    renumberRefs();

    // Suggest genus / species from the scientific name if those are blank
    const sci = document.getElementById("scientific_name");
    sci.addEventListener("blur", function () {
        const genus = document.getElementById("genus");
        const parts = sci.value.trim().split(/\s+/);
        if (!genus.value.trim() && parts[0]) genus.value = parts[0];
    });

    show(0);

})();
