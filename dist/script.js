/*
 * Links de conversão: preencha as duas URLs abaixo antes da publicação final.
 * A página permanece navegável enquanto os links ainda não forem informados.
 */
const CLEIDE_LINKS = {
  calendly: "",
  ebook: ""
};

const header = document.querySelector(".site-header");
const menuButton = document.querySelector(".menu-toggle");
const menu = document.querySelector(".main-nav");
const menuIcon = menuButton?.querySelector("use");
const mobileCta = document.querySelector(".mobile-cta");
const finalSection = document.querySelector("#agendar");
const toast = document.querySelector(".toast");

document.getElementById("current-year").textContent = new Date().getFullYear();

function setMenu(open) {
  menu?.classList.toggle("open", open);
  document.body.classList.toggle("menu-open", open);
  menuButton?.setAttribute("aria-expanded", String(open));
  menuButton?.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
  if (menuIcon) menuIcon.setAttribute("href", open ? "#i-close" : "#i-menu");
}

menuButton?.addEventListener("click", () => setMenu(!menu.classList.contains("open")));
menu?.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => setMenu(false)));
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") setMenu(false);
});

function updateHeader() {
  header?.classList.toggle("scrolled", window.scrollY > 20);
}
updateHeader();
window.addEventListener("scroll", updateHeader, { passive: true });

const revealObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12, rootMargin: "0px 0px -45px" });

document.querySelectorAll(".reveal").forEach((element) => revealObserver.observe(element));

const ctaObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => mobileCta?.classList.toggle("hidden", entry.isIntersecting));
}, { threshold: 0.2 });
if (finalSection) ctaObserver.observe(finalSection);

let toastTimer;
function showToast(message) {
  if (!toast) return;
  toast.textContent = message;
  toast.setAttribute("aria-hidden", "false");
  toast.classList.add("show");
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => {
    toast.classList.remove("show");
    toast.setAttribute("aria-hidden", "true");
  }, 3600);
}

document.querySelectorAll(".js-external").forEach((link) => {
  link.addEventListener("click", (event) => {
    const key = link.dataset.link;
    const destination = CLEIDE_LINKS[key];
    if (destination) {
      link.href = destination;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      return;
    }
    event.preventDefault();
    showToast(key === "ebook"
      ? "O link de compra do E-book Raízes será disponibilizado em breve."
      : "A agenda online será disponibilizada em breve.");
  });
});
