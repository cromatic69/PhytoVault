"use strict";

function initPhytoTable() {

    const table = document.getElementById("phytoTable");

    if (!table) {
        return;
    }

    const tbody = table.querySelector("tbody");
    const allRows = Array.from(tbody.querySelectorAll("tr"));
    const columnCount = table.querySelectorAll("thead th").length;

    if (allRows.length === 0) {
        return;
    }

    const searchInput = document.getElementById("phytoSearch");
    const pageSizeSelect = document.getElementById("phytoPageSize");
    const pagination = document.getElementById("phytoPagination");
    const infoText = document.getElementById("phytoInfo");

    let currentPage = 1;
    let sortColumn = null;
    let sortAsc = true;

    function getFiltered() {

        const keyword = (searchInput.value || "").trim().toLowerCase();

        if (keyword === "") {
            return allRows.slice();
        }

        return allRows.filter(
            row => (row.dataset.search || "").includes(keyword)
        );

    }

    function render() {

        let rows = getFiltered();

        if (sortColumn !== null) {

            rows.sort((a, b) => {

                const av = a.children[sortColumn].textContent.trim().toLowerCase();
                const bv = b.children[sortColumn].textContent.trim().toLowerCase();

                if (av < bv) return sortAsc ? -1 : 1;
                if (av > bv) return sortAsc ? 1 : -1;

                return 0;

            });

        }

        const pageSize = pageSizeSelect.value === "all"
            ? Math.max(rows.length, 1)
            : parseInt(pageSizeSelect.value, 10);

        const totalPages = Math.max(1, Math.ceil(rows.length / pageSize));

        if (currentPage > totalPages) currentPage = totalPages;
        if (currentPage < 1) currentPage = 1;

        const start = (currentPage - 1) * pageSize;
        const end = start + pageSize;

        tbody.innerHTML = "";

        if (rows.length === 0) {

            const tr = document.createElement("tr");
            const td = document.createElement("td");

            td.colSpan = columnCount;
            td.textContent = "No matching phytochemicals found";
            td.style.textAlign = "center";
            td.style.padding = "25px";

            tr.appendChild(td);
            tbody.appendChild(tr);

        } else {

            rows.slice(start, end).forEach(row => tbody.appendChild(row));

        }

        infoText.textContent = rows.length === 0
            ? "Showing 0 entries"
            : `Showing ${start + 1} to ${Math.min(end, rows.length)} of ${rows.length} entries`;

        pagination.innerHTML = "";

        for (let p = 1; p <= totalPages; p++) {

            const btn = document.createElement("button");

            btn.type = "button";
            btn.textContent = p;
            btn.className = "page-number" + (p === currentPage ? " active" : "");

            btn.addEventListener("click", () => {
                currentPage = p;
                render();
            });

            pagination.appendChild(btn);

        }

    }

    searchInput.addEventListener("keyup", () => {
        currentPage = 1;
        render();
    });

    pageSizeSelect.addEventListener("change", () => {
        currentPage = 1;
        render();
    });

    table.querySelectorAll("thead th[data-sort]").forEach((th) => {

        th.style.cursor = "pointer";

        th.addEventListener("click", () => {

            const colIndex = Array.from(th.parentNode.children).indexOf(th);

            if (sortColumn === colIndex) {
                sortAsc = !sortAsc;
            } else {
                sortColumn = colIndex;
                sortAsc = true;
            }

            render();

        });

    });

    render();

}

document.addEventListener("DOMContentLoaded", initPhytoTable);
