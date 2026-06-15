const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function buildStaggeredTitle() {
  const title = document.querySelector(".staggered-title");
  if (!title) return;

  const text = title.dataset.staggerText || "";
  title.textContent = "";
  Array.from(text).forEach((char, index) => {
    const span = document.createElement("span");
    span.className = "stagger-char";
    span.style.setProperty("--char-index", index);
    span.textContent = char === " " ? "\u00a0" : char;
    title.appendChild(span);
  });
}

function setupReveals() {
  const revealTargets = [
    document.querySelector(".nature-inner"),
    ...document.querySelectorAll(".fade-down"),
    ...document.querySelectorAll(".reveal-on-scroll"),
    ...document.querySelectorAll(".anim-item"),
  ].filter(Boolean);

  if (reduceMotion) {
    revealTargets.forEach((target) => target.classList.add("is-visible"));
    document.querySelector(".nature-inner")?.classList.add("is-visible");
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );

  revealTargets.forEach((target) => observer.observe(target));
}

function setupNatureVideoBoomerang() {
  const video = document.querySelector(".nature-video");
  const canvas = document.querySelector(".nature-canvas");
  if (!video || !canvas || reduceMotion) return;

  const context = canvas.getContext("2d");
  if (!context) return;

  const frames = [];
  let ready = false;
  let direction = 1;
  let index = 0;
  let lastTime = 0;

  function captureFrame() {
    if (ready || video.videoWidth === 0 || video.videoHeight === 0) return;
    const maxWidth = 960;
    const scale = Math.min(1, maxWidth / video.videoWidth);
    const width = Math.max(1, Math.round(video.videoWidth * scale));
    const height = Math.max(1, Math.round(video.videoHeight * scale));
    const frame = document.createElement("canvas");
    frame.width = width;
    frame.height = height;
    const frameContext = frame.getContext("2d");
    if (frameContext) {
      frameContext.drawImage(video, 0, 0, width, height);
      frames.push(frame);
    }
  }

  function drawFrame(timestamp) {
    if (!ready || frames.length === 0) return;
    requestAnimationFrame(drawFrame);
    if (timestamp - lastTime < 33) return;
    lastTime = timestamp;

    const frame = frames[index];
    canvas.width = canvas.clientWidth || window.innerWidth;
    canvas.height = canvas.clientHeight || Math.max(1, window.innerHeight - 200);
    context.drawImage(frame, 0, 0, canvas.width, canvas.height);

    index += direction;
    if (index >= frames.length - 1) {
      index = frames.length - 1;
      direction = -1;
    } else if (index <= 0) {
      index = 0;
      direction = 1;
    }
  }

  const captureInterval = setInterval(captureFrame, 1000 / 60);
  video.addEventListener("ended", () => {
    clearInterval(captureInterval);
    if (frames.length < 4) {
      video.loop = true;
      video.play().catch(() => {});
      return;
    }
    ready = true;
    video.style.display = "none";
    canvas.style.display = "block";
    requestAnimationFrame(drawFrame);
  });

  setTimeout(() => {
    if (!ready && frames.length > 18) {
      ready = true;
      clearInterval(captureInterval);
      video.style.display = "none";
      canvas.style.display = "block";
      requestAnimationFrame(drawFrame);
    }
  }, 5000);
}

function setupContactForm() {
  const tags = document.querySelectorAll("[data-service-tags] button");
  tags.forEach((tag) => {
    tag.addEventListener("click", () => {
      tag.classList.toggle("active");
    });
  });

  const form = document.querySelector(".contact-form");
  const card = document.querySelector("[data-form-card]");
  if (!form || !card) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = form.querySelector(".submit-button");
    if (button) {
      button.disabled = true;
      button.textContent = "Wird gesendet...";
    }
    await new Promise((resolve) => setTimeout(resolve, 1000));
    card.innerHTML = `
      <div class="success-state">
        <div class="success-check">✓</div>
        <h3>Alles angekommen!</h3>
        <p>Wir melden uns innerhalb von 24 Stunden.</p>
      </div>
    `;
  });
}

buildStaggeredTitle();
setupReveals();
setupNatureVideoBoomerang();
setupContactForm();
