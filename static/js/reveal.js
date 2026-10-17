"use strict";

document.addEventListener("DOMContentLoaded", function () {

    // ==========================
    // Scroll reveal
    // ==========================
    const revealEls = document.querySelectorAll(".reveal");

    if (revealEls.length > 0) {

        if ("IntersectionObserver" in window) {

            const observer = new IntersectionObserver(
                function (entries, obs) {

                    entries.forEach(function (entry) {

                        if (entry.isIntersecting) {

                            entry.target.classList.add("in-view");
                            obs.unobserve(entry.target);

                        }

                    });

                },
                { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
            );

            revealEls.forEach(function (el) {
                observer.observe(el);
            });

        } else {

            // No IntersectionObserver support: just show everything.
            revealEls.forEach(function (el) {
                el.classList.add("in-view");
            });

        }

    }

    // ==========================
    // Animated counters
    // ==========================
    const counters = document.querySelectorAll(".counter");

    if (counters.length > 0) {

        function animateCounter(el) {

            const target = parseInt(el.dataset.target, 10) || 0;
            const duration = 1400;
            const start = performance.now();

            function step(now) {

                const progress = Math.min((now - start) / duration, 1);
                const eased = 1 - Math.pow(1 - progress, 3);

                el.textContent = Math.floor(eased * target).toLocaleString();

                if (progress < 1) {
                    requestAnimationFrame(step);
                } else {
                    el.textContent = target.toLocaleString();
                }

            }

            requestAnimationFrame(step);

        }

        if ("IntersectionObserver" in window) {

            const counterObserver = new IntersectionObserver(
                function (entries, obs) {

                    entries.forEach(function (entry) {

                        if (entry.isIntersecting) {

                            animateCounter(entry.target);
                            obs.unobserve(entry.target);

                        }

                    });

                },
                { threshold: 0.4 }
            );

            counters.forEach(function (el) {
                counterObserver.observe(el);
            });

        } else {

            counters.forEach(animateCounter);

        }

    }

});
