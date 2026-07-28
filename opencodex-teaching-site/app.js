window.mermaid?.initialize({
  startOnLoad: true,
  theme: "base",
  securityLevel: "strict",
  themeVariables: {
    primaryColor: "#1e40af",
    primaryTextColor: "#111827",
    primaryBorderColor: "#3b82f6",
    lineColor: "#6b7280",
    secondaryColor: "#fef3c7",
    tertiaryColor: "#d1fae5",
    background: "#ffffff",
    mainBkg: "#ffffff",
    secondBkg: "#f9fafb",
    tertiaryBkg: "#f3f4f6"
  },
  flowchart: { useMaxWidth: true, htmlLabels: true, curve: "basis" },
  sequence: {
    useMaxWidth: true,
    diagramMarginX: 50,
    diagramMarginY: 10,
    actorMargin: 50,
    width: 150,
    height: 65,
    boxMargin: 10,
    boxTextMargin: 5,
    noteMargin: 10,
    messageMargin: 35
  }
});

const sections = document.querySelectorAll("section[id]");
const tocLinks = document.querySelectorAll(".toc-link");
const menuButton = document.querySelector("#menu-button");
const primaryNav = document.querySelector("#primary-nav");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    const id = entry.target.getAttribute("id");
    tocLinks.forEach((link) => {
      link.classList.toggle("active", link.getAttribute("href") === `#${id}`);
    });
  });
}, { rootMargin: "-100px 0px -66%" });

sections.forEach((section) => observer.observe(section));

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener("click", (event) => {
    const target = document.querySelector(link.getAttribute("href"));
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
    primaryNav?.classList.remove("mobile-nav-open");
    menuButton?.setAttribute("aria-expanded", "false");
  });
});

menuButton?.addEventListener("click", () => {
  const expanded = menuButton.getAttribute("aria-expanded") === "true";
  menuButton.setAttribute("aria-expanded", String(!expanded));
  primaryNav?.classList.toggle("mobile-nav-open", !expanded);
});
