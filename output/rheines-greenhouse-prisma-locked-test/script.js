const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function splitWords(element) {
  const text = element.textContent.trim();
  const addAsterisk = element.dataset.asterisk === "true";
  element.textContent = "";

  text.split(/\s+/).forEach((word, index, words) => {
    const span = document.createElement("span");
    span.className = "word";
    span.style.setProperty("--word-index", index);
    span.textContent = word;

    if (addAsterisk && index === words.length - 1) {
      const star = document.createElement("span");
      star.className = "asterisk";
      star.textContent = "*";
      span.appendChild(star);
    }

    element.appendChild(span);
    if (index < words.length - 1) {
      element.appendChild(document.createTextNode(" "));
    }
  });
}

function splitMultiWords(element) {
  const nodes = Array.from(element.children);
  element.textContent = "";
  let wordIndex = 0;

  nodes.forEach((node, nodeIndex) => {
    const wrapper = node.tagName.toLowerCase() === "em" ? document.createElement("em") : document.createElement("span");
    wrapper.className = node.className || "";
    node.textContent.trim().split(/\s+/).forEach((word, index, words) => {
      const span = document.createElement("span");
      span.className = "word";
      span.style.setProperty("--word-index", wordIndex);
      span.textContent = word;
      wrapper.appendChild(span);
      wordIndex += 1;
      if (index < words.length - 1) wrapper.appendChild(document.createTextNode(" "));
    });
    element.appendChild(wrapper);
    if (nodeIndex < nodes.length - 1) element.appendChild(document.createTextNode(" "));
  });
}

function splitLetters(element) {
  const text = element.textContent;
  element.textContent = "";
  Array.from(text).forEach((char, index) => {
    const span = document.createElement("span");
    span.className = "letter";
    span.dataset.index = index;
    span.textContent = char;
    element.appendChild(span);
  });
}

document.querySelectorAll(".words-pull-up").forEach(splitWords);
document.querySelectorAll(".multi-words").forEach(splitMultiWords);
document.querySelectorAll(".letters-reveal").forEach(splitLetters);

document.querySelectorAll(".reveal-card").forEach((card, index) => {
  card.style.setProperty("--card-index", index);
});

if (prefersReducedMotion) {
  document.querySelectorAll(".words-pull-up, .multi-words, .fade-up, .reveal-card").forEach((element) => {
    element.classList.add("is-visible");
  });
  document.querySelectorAll(".letter").forEach((letter) => {
    letter.style.opacity = "1";
  });
} else {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.2, rootMargin: "0px 0px -100px 0px" }
  );

  document.querySelectorAll(".words-pull-up, .multi-words, .fade-up, .reveal-card").forEach((element) => {
    observer.observe(element);
  });

  const aboutText = document.querySelector(".letters-reveal");
  const letters = Array.from(document.querySelectorAll(".letter"));

  function updateLetters() {
    if (!aboutText || letters.length === 0) return;
    const rect = aboutText.getBoundingClientRect();
    const viewport = window.innerHeight || document.documentElement.clientHeight;
    const start = viewport * 0.8;
    const end = viewport * 0.2;
    const progress = Math.min(1, Math.max(0, (start - rect.top) / (start - end + rect.height)));

    letters.forEach((letter, index) => {
      const charProgress = index / letters.length;
      const localStart = charProgress - 0.1;
      const localEnd = charProgress + 0.05;
      const local = Math.min(1, Math.max(0, (progress - localStart) / (localEnd - localStart)));
      letter.style.opacity = String(0.2 + local * 0.8);
    });
  }

  updateLetters();
  window.addEventListener("scroll", updateLetters, { passive: true });
  window.addEventListener("resize", updateLetters);
}
