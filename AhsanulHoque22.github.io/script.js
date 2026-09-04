/* GSAP/ScrollTrigger/Lenis all load from CDN. If any of them fail (ad
   blocker, network), this whole block throws on the first line. Isolate it
   so a failure here can't take out the canvas background, mobile nav, and
   scroll reveals below, which don't depend on GSAP at all. */
try {
  gsap.registerPlugin(ScrollTrigger);

  /* ---------- Lenis smooth scroll wired to GSAP ticker ---------- */
  const lenis = new Lenis({ duration: 1.1, smoothWheel: true });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((time) => lenis.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);
  window.__lenis = lenis; /* exposed so the file-drawer section can scrollTo an index */

  /* ---------- Scroll progress bar ---------- */
  gsap.to('#progress-bar', {
    width: '100%',
    ease: 'none',
    scrollTrigger: { trigger: document.body, start: 'top top', end: 'bottom bottom', scrub: true }
  });

  /* ---------- Nav background on scroll ---------- */
  ScrollTrigger.create({
    start: 100,
    onUpdate: (self) => document.getElementById('navbar').classList.toggle('scrolled', self.scroll() > 100)
  });

  /* Hero entrance: the .hero-card itself is a .reveal-up element (see the
     generic IntersectionObserver below), so it fades/slides in on load
     without needing its own bespoke GSAP timeline. */

  /* ---------- Hero parallax: each layer drifts upward at its own rate
     as the hero scrolls past, background layers slower than foreground
     ones, for a sense of depth. Scoped to #hero's own scroll range and
     clipped by .hero-card's overflow:hidden, so nothing leaks into the
     section below. ---------- */
  if (document.getElementById('hero')) {
    gsap.timeline({
      scrollTrigger: { trigger: '#hero', start: 'top top', end: 'bottom top', scrub: 0.3 }
    })
      .to('[data-parallax-layer="1"]', { yPercent: -10, ease: 'none' }, 0) /* ticker: furthest back */
      .to('[data-parallax-layer="2"]', { yPercent: -20, ease: 'none' }, 0) /* big background word */
      .to('[data-parallax-layer="3"]', { yPercent: -35, ease: 'none' }, 0) /* portrait: closest */
      .to('[data-parallax-layer="4"]', { yPercent: -15, ease: 'none' }, 0); /* role title */
  }
} catch (e) {
  console.error('GSAP failed to load. Animations disabled, rest of the page still works:', e);
}

/* ---------- Generic reveal-on-scroll (IntersectionObserver: no dependency
   on ScrollTrigger's scroll-position sync with Lenis, so it can't get stuck
   if that sync ever drifts) ---------- */
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.15, rootMargin: '0px 0px -10% 0px' });
document.querySelectorAll('.reveal-up').forEach((el) => revealObserver.observe(el));

/* ---------- Count-up stats ---------- */
const statObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    statObserver.unobserve(entry.target);
    const el = entry.target;
    const target = parseFloat(el.dataset.count);
    if (typeof gsap === 'undefined') { el.textContent = target % 1 === 0 ? target : target.toFixed(2); return; }
    const obj = { val: 0 };
    gsap.to(obj, {
      val: target,
      duration: 1.6,
      ease: 'power2.out',
      onUpdate: () => (el.textContent = target % 1 === 0 ? Math.floor(obj.val) : obj.val.toFixed(2)),
    });
  });
}, { threshold: 0.3 });
document.querySelectorAll('.stat-num').forEach((el) => statObserver.observe(el));

/* ---------- Safety net: if any reveal element is somehow never observed
   (e.g. already in view before JS ran), reveal everything after 1.5s ---------- */
setTimeout(() => document.querySelectorAll('.reveal-up:not(.is-visible)').forEach((el) => el.classList.add('is-visible')), 1500);

/* ---------- Project card hover tilt-lite ---------- */
if (typeof gsap !== 'undefined') {
  document.querySelectorAll('.project-card').forEach((card) => {
    card.addEventListener('mousemove', (e) => {
      const r = card.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width - 0.5) * 6;
      gsap.to(card, { rotateX: -x * 0.3, rotateY: x, duration: 0.4, transformPerspective: 800 });
    });
    card.addEventListener('mouseleave', () => gsap.to(card, { rotateX: 0, rotateY: 0, duration: 0.6 }));
  });
}

/* ---------- Mobile nav toggle ---------- */
const navToggle = document.getElementById('nav-toggle');
const navLinks = document.querySelector('.nav-links');
navToggle.addEventListener('click', () => {
  navLinks.classList.toggle('open');
  navToggle.classList.toggle('active');
});
navLinks.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => {
  navLinks.classList.remove('open');
  navToggle.classList.remove('active');
}));

/* ---------- Canvas: constellation / particle network background ---------- */
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
/* named bgW/bgH, not w/h: Lenis's dist build isn't IIFE-wrapped and
   declares a top-level `function w(...)`, so a global `let w` here
   collides with it, causing a SyntaxError that takes this whole file down. */
let bgW, bgH, particles;
const mouse = { x: -9999, y: -9999 };

function resize() {
  bgW = canvas.width = window.innerWidth;
  bgH = canvas.height = window.innerHeight;
  const count = Math.min(90, Math.floor((bgW * bgH) / 18000));
  particles = Array.from({ length: count }, () => ({
    x: Math.random() * bgW,
    y: Math.random() * bgH,
    vx: (Math.random() - 0.5) * 0.3,
    vy: (Math.random() - 0.5) * 0.3,
  }));
}
window.addEventListener('resize', resize);
window.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });
resize();

function tick() {
  ctx.clearRect(0, 0, bgW, bgH);
  for (const p of particles) {
    p.x += p.vx; p.y += p.vy;
    if (p.x < 0 || p.x > bgW) p.vx *= -1;
    if (p.y < 0 || p.y > bgH) p.vy *= -1;
    const dx = p.x - mouse.x, dy = p.y - mouse.y;
    const dist = Math.sqrt(dx * dx + dy * dy);
    if (dist < 140) { p.x += dx / dist * 0.6; p.y += dy / dist * 0.6; }
  }
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const a = particles[i], b = particles[j];
      const d = Math.hypot(a.x - b.x, a.y - b.y);
      if (d < 140) {
        ctx.strokeStyle = `rgba(77,243,255,${0.12 * (1 - d / 140)})`;
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
      }
    }
    ctx.fillStyle = 'rgba(155,107,255,0.6)';
    ctx.beginPath(); ctx.arc(particles[i].x, particles[i].y, 1.6, 0, Math.PI * 2); ctx.fill();
  }
  requestAnimationFrame(tick);
}
tick();

/* FILE STACK: a cascading stack of manila-folder-shaped project files.
   Content is built once from the hidden .project-data cards (single
   source of truth). Every file is just a shape and a title, nothing
   toggles open: scrolling moves a glowing "selected" highlight through
   the stack, and clicking a file navigates straight to its project
   link (same as clicking the link itself). */
(function () {
  const track = document.getElementById('drawer-scroll-track');
  const pin = document.querySelector('.drawer-pin');
  const stack = document.getElementById('folder-stack');
  const cards = document.querySelectorAll('.project-data .project-card');
  if (!track || !pin || !stack || !cards.length) return;

  const n = cards.length;

  /* ---- build files from the hidden data cards (no duplicated content) ---- */
  cards.forEach((card, i) => {
    const h3 = card.querySelector('.project-info h3');
    const link = card.querySelector('.project-links a');

    const folder = document.createElement('div');
    folder.className = 'folder';
    folder.dataset.index = String(i);
    if (link) {
      folder.title = 'Open ' + (h3 ? h3.textContent.trim() : 'project') + ' ↗';
    }

    const tabRow = document.createElement('div');
    tabRow.className = 'folder-tab-row';
    tabRow.innerHTML =
      '<span class="folder-num">' + String(i + 1).padStart(2, '0') + '</span>' +
      '<span class="folder-title">' + (h3 ? h3.textContent.trim() : '') + '</span>';
    folder.appendChild(tabRow);

    if (link) {
      folder.addEventListener('click', () => window.open(link.href, '_blank', 'noopener'));
    } else {
      folder.style.cursor = 'default';
    }

    stack.appendChild(folder);
  });

  const folders = Array.from(stack.children);
  const isMobile = () => window.matchMedia('(max-width:860px)').matches;

  /* ---- mobile: plain static stack, no scroll rig; click still opens
     the project link the same as on desktop. ---- */
  function wireMobile() {}

  /* ---- desktop ---- */
  const STEP = 48; /* vertical stagger between cascading files */
  let hoverIndex = -1;

  function layout() {
    /* +40vh settle buffer at the end: without it, momentum scroll can carry
       a few pixels past the exact instant position:sticky releases while
       progress is still clamped to 1, leaving the last file rendered as
       if still pinned even though its container already scrolled away. */
    track.style.height = (150 + n * 20 + 40) + 'vh';
  }

  function scrollProgress() {
    const trackRect = track.getBoundingClientRect();
    /* Subtract the settle buffer so progress reaches 1 a bit before the
       track's true end, leaving slack scroll room where the last file
       stays fully settled (and the section still pinned) instead of
       sitting exactly on the position:sticky release boundary. */
    const total = trackRect.height - window.innerHeight - window.innerHeight * 0.4;
    return total > 0 ? Math.min(1, Math.max(0, -trackRect.top / total)) : 0;
  }

  function render() {
    const progress = scrollProgress();
    const nearestIdx = Math.round(progress * (n - 1));
    const selectedIdx = hoverIndex >= 0 ? hoverIndex : nearestIdx;

    folders.forEach((folder, i) => {
      const isSelected = i === selectedIdx;
      const ty = i * STEP + (isSelected ? -8 : 0);

      folder.classList.toggle('is-selected', isSelected);
      folder.style.transform =
        'translateX(-50%) translateY(' + ty + 'px)' + (isSelected ? ' scale(1.04)' : '');
      folder.style.zIndex = String(100 + i); /* later files sit in front */
    });
  }

  function wireDesktop() {
    layout();
    let ticking = false;
    const onScroll = () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => { render(); ticking = false; });
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', () => { layout(); render(); });
    folders.forEach((folder, i) => {
      folder.addEventListener('mouseenter', () => { hoverIndex = i; render(); });
      folder.addEventListener('mouseleave', () => { hoverIndex = -1; render(); });
    });
    render();
  }

  let mobileMode = isMobile();
  if (mobileMode) wireMobile(); else wireDesktop();
  window.addEventListener('resize', () => {
    const nowMobile = isMobile();
    if (nowMobile !== mobileMode) {
      mobileMode = nowMobile;
      folders.forEach((f) => {
        f.style.transform = ''; f.style.zIndex = '';
        f.classList.remove('is-selected');
      });
      track.style.height = '';
      if (mobileMode) wireMobile(); else wireDesktop();
    }
  });
})();
