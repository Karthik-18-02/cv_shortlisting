//  static/scripts/script.js
// Theme Toggle Module
const ThemeToggle = (() => {
  const toggleButton = document.getElementById("theme-toggle");
  const root = document.documentElement;

  const setTheme = (theme) => {
    root.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  };

  const toggleTheme = () => {
    const current = root.getAttribute("data-theme") || "light";
    setTheme(current === "light" ? "dark" : "light");
  };

  const init = () => {
    const saved = localStorage.getItem("theme") || "light";
    setTheme(saved);
    if (toggleButton) toggleButton.addEventListener("click", toggleTheme);
  };

  return { init };
})();

// Smooth Scroll for Navigation Links
const SmoothScroll = (() => {
  const links = document.querySelectorAll('a[href^="#"]');

  const scrollToSection = (e) => {
    e.preventDefault();
    const target = document.querySelector(e.currentTarget.getAttribute("href"));
    if (target) target.scrollIntoView({ behavior: "smooth" });
  };

  const init = () => {
    links.forEach((link) => link.addEventListener("click", scrollToSection));
  };

  return { init };
})();

// Scroll Reveal Animations using IntersectionObserver
const ScrollReveal = (() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("reveal-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );

  const init = () => {
    document.querySelectorAll(".reveal").forEach((el) => observer.observe(el));
  };

  return { init };
})();

// File Upload with Progress Feedback
const FileUpload = (() => {
  const form = document.querySelector(".upload-form");
  const input = document.getElementById("resume-upload");
  const progressBar = document.getElementById("progress-bar");
  const progressText = document.getElementById("progress-text");

  const handleUpload = () => {
    const file = input.files[0];
    if (!file || file.type !== "application/pdf") return;

    const xhr = new XMLHttpRequest();
    const data = new FormData(form);
    xhr.open("POST", form.action);
    xhr.upload.addEventListener("progress", (e) => {
      const percent = Math.round((e.loaded / e.total) * 100);
      progressBar.style.width = percent + "%";
      progressText.textContent = percent + "%";
    });
    xhr.onload = () => window.location.reload();
    xhr.send(data);
  };

  const init = () => {
    if (!form) return;
    input.addEventListener("change", handleUpload);
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      handleUpload();
    });
  };

  return { init };
})();

// Dynamic Metrics Counter
const Counter = (() => {
  const runCounter = (el) => {
    const target = +el.getAttribute("data-target");
    const step = target / 200;
    let count = 0;
    const update = () => {
      count += step;
      if (count < target) {
        el.textContent = Math.floor(count);
        requestAnimationFrame(update);
      } else {
        el.textContent = target;
      }
    };
    update();
  };

  const init = () => {
    const counters = document.querySelectorAll(".metric-number");
    counters.forEach((el) => {
      ScrollReveal.init(); // ensure reveal
      if (el.classList.contains("reveal-visible")) runCounter(el);
    });
  };

  return { init };
})();

// Mobile Menu Toggle
const MobileNav = (() => {
  const toggle = document.getElementById("mobile-toggle");
  const nav = document.querySelector(".nav-links");

  const init = () => {
    if (!toggle) return;
    toggle.addEventListener("click", () => {
      nav.classList.toggle("nav-open");
    });
  };

  return { init };
})();

// Initialize all modules on DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  ThemeToggle.init();
  SmoothScroll.init();
  ScrollReveal.init();
  FileUpload.init();
  Counter.init();
  MobileNav.init();
});

document.getElementById("drop-zone").addEventListener("click", function() {
  document.getElementById("resume-upload").click(); // This will open the file dialog when the container is clicked
});

