const initializeCourseNavigation = () => {
  const desktop = window.matchMedia("(min-width: 981px)");

  document.querySelectorAll(".site-header").forEach((header) => {
    const toggle = header.querySelector(".menu-toggle");
    const nav = header.querySelector(".nav");
    if (!toggle || !nav) return;

    const closeMenu = () => {
      header.dataset.menuOpen = "false";
      toggle.setAttribute("aria-expanded", "false");
    };

    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") !== "true";
      header.dataset.menuOpen = String(open);
      toggle.setAttribute("aria-expanded", String(open));
    });

    nav.addEventListener("click", (event) => {
      if (event.target.closest("a")) closeMenu();
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        closeMenu();
        toggle.focus();
      }
    });

    desktop.addEventListener("change", (event) => {
      if (event.matches) closeMenu();
    });
  });
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initializeCourseNavigation, { once: true });
} else {
  initializeCourseNavigation();
}
