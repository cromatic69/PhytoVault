"use strict";

function escapeXml(str) {

    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");

}

function hexagonPoints(cx, cy, r) {

    const points = [];

    for (let i = 0; i < 6; i++) {

        const angle = (Math.PI / 3) * i - Math.PI / 2;

        points.push(
            (cx + r * Math.cos(angle)).toFixed(1) + "," +
            (cy + r * Math.sin(angle)).toFixed(1)
        );

    }

    return points.join(" ");

}

function initPlantNetwork() {

    const dataEl = document.getElementById("networkData");
    const container = document.getElementById("networkGraph");

    if (!dataEl || !container) {
        return;
    }

    let data;

    try {
        data = JSON.parse(dataEl.textContent);
    } catch (err) {
        return;
    }

    const nodes = data.phytochemicals || [];
    const plantName = data.plantName || "Plant";

    if (nodes.length === 0) {

        container.innerHTML =
            '<p class="muted" style="padding:40px;text-align:center;">' +
            'No phytochemical associations recorded yet.</p>';

        return;

    }

    const width = 560;
    const height = 400;
    const cx = width / 2;
    const cy = height / 2;
    const radius = Math.min(width, height) / 2 - 55;

    let svg = `<svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg">`;

    // Edges (drawn first, so nodes sit on top)
    nodes.forEach((node, i) => {

        const angle = (2 * Math.PI * i) / nodes.length;
        const x = cx + radius * Math.cos(angle);
        const y = cy + radius * Math.sin(angle);

        svg += `<line x1="${cx}" y1="${cy}" x2="${x.toFixed(1)}" y2="${y.toFixed(1)}" ` +
               `stroke="#c9d6c9" stroke-width="1.5"/>`;

    });

    // Center node (the plant)
    svg += `<circle cx="${cx}" cy="${cy}" r="15" fill="#1565C0"/>`;
    svg += `<text x="${cx}" y="${cy + 34}" text-anchor="middle" class="network-center-label">` +
           `${escapeXml(plantName)}</text>`;

    // Outer nodes (phytochemicals)
    nodes.forEach((node, i) => {

        const angle = (2 * Math.PI * i) / nodes.length;
        const x = cx + radius * Math.cos(angle);
        const y = cy + radius * Math.sin(angle);

        const cos = Math.cos(angle);
        const sin = Math.sin(angle);

        const anchor = cos > 0.15 ? "start" : (cos < -0.15 ? "end" : "middle");
        const labelX = x + (cos > 0.15 ? 10 : (cos < -0.15 ? -10 : 0));
        const labelY = y + (sin > 0 ? 16 : -10);

        svg += `<g class="network-node" data-href="/phytochemical/${node.id}">`;
        svg += `<polygon points="${hexagonPoints(x, y, 9)}" fill="#2E7D32"/>`;
        svg += `<text x="${labelX.toFixed(1)}" y="${labelY.toFixed(1)}" text-anchor="${anchor}" ` +
               `class="network-node-label">${escapeXml(node.name)}</text>`;
        svg += `</g>`;

    });

    svg += `</svg>`;

    container.innerHTML = svg;

    container.querySelectorAll(".network-node").forEach(node => {

        node.style.cursor = "pointer";

        node.addEventListener("click", () => {
            window.location.href = node.getAttribute("data-href");
        });

    });

}

document.addEventListener("DOMContentLoaded", initPlantNetwork);
