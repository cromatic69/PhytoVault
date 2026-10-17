"use strict";

const PhytoDialog = (function () {

    function ensureToastContainer() {

        let container = document.getElementById("pv-toast-container");

        if (!container) {
            container = document.createElement("div");
            container.id = "pv-toast-container";
            document.body.appendChild(container);
        }

        return container;

    }

    function toast(message, type, duration) {

        if (!message) {
            return;
        }

        type = type || "info";
        duration = duration === undefined ? 4500 : duration;

        const icons = { success: "✅", error: "⚠️", info: "ℹ️" };

        const container = ensureToastContainer();

        const el = document.createElement("div");

        el.className = "pv-toast pv-toast-" + type;

        const iconSpan = document.createElement("span");
        iconSpan.className = "pv-toast-icon";
        iconSpan.textContent = icons[type] || icons.info;

        const msgSpan = document.createElement("span");
        msgSpan.className = "pv-toast-message";
        msgSpan.textContent = message;

        const closeBtn = document.createElement("button");
        closeBtn.className = "pv-toast-close";
        closeBtn.setAttribute("aria-label", "Close");
        closeBtn.innerHTML = "&times;";

        el.appendChild(iconSpan);
        el.appendChild(msgSpan);
        el.appendChild(closeBtn);

        container.appendChild(el);

        requestAnimationFrame(() => el.classList.add("show"));

        const remove = () => {
            el.classList.remove("show");
            setTimeout(() => el.remove(), 300);
        };

        closeBtn.addEventListener("click", remove);

        if (duration > 0) {
            setTimeout(remove, duration);
        }

    }

    function confirmDialog(message, options) {

        options = options || {};

        return new Promise((resolve) => {

            const overlay = document.createElement("div");
            overlay.className = "pv-modal-overlay";

            const modal = document.createElement("div");
            modal.className = "pv-modal";

            const icon = document.createElement("div");
            icon.className = "pv-modal-icon";
            icon.textContent = options.icon || (options.danger ? "🗑️" : "❓");

            const msg = document.createElement("p");
            msg.className = "pv-modal-message";
            msg.textContent = message;

            const actions = document.createElement("div");
            actions.className = "pv-modal-actions";

            const cancelBtn = document.createElement("button");
            cancelBtn.className = "pv-modal-cancel";
            cancelBtn.textContent = options.cancelText || "Cancel";

            const confirmBtn = document.createElement("button");
            confirmBtn.className = "pv-modal-confirm";
            confirmBtn.textContent = options.confirmText || "Confirm";

            if (options.danger) {
                confirmBtn.style.background = "#C62828";
            }

            actions.appendChild(cancelBtn);
            actions.appendChild(confirmBtn);

            modal.appendChild(icon);
            modal.appendChild(msg);
            modal.appendChild(actions);

            overlay.appendChild(modal);
            document.body.appendChild(overlay);

            requestAnimationFrame(() => overlay.classList.add("show"));

            const cleanup = (result) => {
                overlay.classList.remove("show");
                setTimeout(() => overlay.remove(), 200);
                resolve(result);
            };

            cancelBtn.addEventListener("click", () => cleanup(false));
            confirmBtn.addEventListener("click", () => cleanup(true));

            overlay.addEventListener("click", (e) => {
                if (e.target === overlay) {
                    cleanup(false);
                }
            });

        });

    }

    function bindConfirmActions() {

        // Links that should ask for confirmation before navigating,
        // e.g. <a href="/admin/delete/3" data-confirm="Delete this plant?" data-danger>
        document.querySelectorAll("a[data-confirm]").forEach((link) => {

            link.addEventListener("click", function (e) {

                e.preventDefault();

                const message = link.getAttribute("data-confirm");
                const href = link.getAttribute("href");

                confirmDialog(message, {
                    danger: link.hasAttribute("data-danger"),
                    confirmText: link.dataset.confirmText || "Confirm"
                }).then((ok) => {
                    if (ok) {
                        window.location.href = href;
                    }
                });

            });

        });

        // Forms that should ask for confirmation before submitting,
        // e.g. <form data-confirm="Remove this admin?" data-danger>
        document.querySelectorAll("form[data-confirm]").forEach((form) => {

            form.addEventListener("submit", function (e) {

                if (form.dataset.pvConfirmed === "true") {
                    return;
                }

                e.preventDefault();

                const message = form.getAttribute("data-confirm");

                confirmDialog(message, {
                    danger: form.hasAttribute("data-danger"),
                    confirmText: form.dataset.confirmText || "Confirm"
                }).then((ok) => {
                    if (ok) {
                        form.dataset.pvConfirmed = "true";
                        form.submit();
                    }
                });

            });

        });

    }

    function classifyMessage(message) {

        const lower = message.toLowerCase();

        const errorPattern = /fail|error|invalid|already|can'?t|cannot|denied|must remain|not found|no accounts?/;
        const successPattern = /success|added|updated|deleted|removed|promoted|welcome/;

        if (errorPattern.test(lower)) {
            return "error";
        }

        if (successPattern.test(lower)) {
            return "success";
        }

        return "info";

    }

    function showFlashedMessages() {

        const el = document.getElementById("pv-flash-data");

        if (!el) {
            return;
        }

        let messages = [];

        try {
            messages = JSON.parse(el.textContent);
        } catch (err) {
            return;
        }

        messages.forEach((message) => toast(message, classifyMessage(message)));

    }

    document.addEventListener("DOMContentLoaded", () => {
        bindConfirmActions();
        showFlashedMessages();
    });

    return {
        toast: toast,
        confirm: confirmDialog
    };

})();
