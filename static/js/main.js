document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".score-card");

    cards.forEach((card, index) => {
        card.style.opacity = "0";
        card.style.transform = "translateY(8px)";

        setTimeout(() => {
            card.style.transition = "opacity 300ms ease, transform 300ms ease";
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
        }, 90 * (index + 1));
    });
});
