document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".score-card");
    const dashboardPanel = document.querySelector("[data-dashboard-panel]");
    const kpiTriggers = document.querySelectorAll(".kpi-trigger");

    cards.forEach((card, index) => {
        card.style.opacity = "0";
        card.style.transform = "translateY(8px)";

        setTimeout(() => {
            card.style.transition = "opacity 300ms ease, transform 300ms ease";
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
        }, 90 * (index + 1));
    });

    if (dashboardPanel && kpiTriggers.length > 0) {
        const titleEl = dashboardPanel.querySelector("[data-kpi-title]");
        const detailEl = dashboardPanel.querySelector("[data-kpi-detail]");
        const scoreEl = dashboardPanel.querySelector("[data-kpi-score]");
        const bandEl = dashboardPanel.querySelector("[data-kpi-band]");

        const updateDashboardPanel = (trigger) => {
            if (!titleEl || !detailEl || !scoreEl || !bandEl) {
                return;
            }

            titleEl.textContent = trigger.dataset.kpiName || "";
            detailEl.textContent = trigger.dataset.kpiDetail || "";
            scoreEl.textContent = trigger.dataset.kpiScore || "";
            bandEl.textContent = trigger.dataset.kpiBand || "";

            kpiTriggers.forEach((item) => {
                const isActive = item === trigger;
                item.setAttribute("aria-pressed", String(isActive));
                item.closest(".dashboard-kpi-card")?.classList.toggle("is-active", isActive);
            });
        };

        kpiTriggers.forEach((trigger) => {
            trigger.addEventListener("click", () => updateDashboardPanel(trigger));
        });
    }
});
