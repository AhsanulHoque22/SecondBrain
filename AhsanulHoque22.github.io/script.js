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

  /* ---------- Hero entrance ---------- */
  gsap.timeline({ defaults: { ease: 'power4.out' } })
    .fromTo('.hero-title .line', { yPercent: 100, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 1, stagger: 0.12 }, 0.1)
    .to('.reveal-line', { opacity: 1, y: 0, duration: 0.8, stagger: 0.1 }, 0.5);
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

/* 3D FILE DRAWER: a physical-feeling stack of project folders.
   Content is built once from the hidden .project-data cards (single
   source of truth). Scrolling only gives the collapsed stack a subtle
   ambient riffle (perspective fade/shrink with distance); nothing opens
   on its own. Clicking a folder is the only thing that expands it into
   its full detail card, rising to the top; clicking it again (or another
   folder) closes it. */
(function () {
  const track = document.getElementById('drawer-scroll-track');
  const stack = document.getElementById('folder-stack');
  const cards = document.querySelectorAll('.project-data .project-card');
  if (!track || !stack || !cards.length) return;

  const n = cards.length;

  /* ---- build folders from the hidden data cards (no duplicated content) ---- */
  cards.forEach((card, i) => {
    const h3 = card.querySelector('.project-info h3');
    const img = card.querySelector('.project-poster');
    const p = card.querySelector('.project-info p');
    const tags = card.querySelector('.tag-row');
    const link = card.querySelector('.project-links a');
    const noLink = card.querySelector('.project-links .no-link');

    const folder = document.createElement('div');
    folder.className = 'folder';
    folder.dataset.index = String(i);

    const tabRow = document.createElement('div');
    tabRow.className = 'folder-tab-row';
    tabRow.innerHTML =
      '<span class="folder-num">' + String(i + 1).padStart(2, '0') + '</span>' +
      '<span class="folder-title">' + (h3 ? h3.textContent.trim() : '') + '</span>';
    folder.appendChild(tabRow);

    const detail = document.createElement('div');
    detail.className = 'folder-detail';
    if (img) {
      const im = document.createElement('img');
      im.className = 'folder-thumb';
      im.src = img.getAttribute('src');
      im.alt = img.getAttribute('alt') || '';
      im.loading = 'lazy';
      detail.appendChild(im);
    }
    if (p) {
      const desc = document.createElement('p');
      desc.className = 'folder-desc';
      desc.textContent = p.textContent.replace(/\s+/g, ' ').trim();
      detail.appendChild(desc);
    }
    if (tags) {
      const row = document.createElement('div');
      row.className = 'folder-tags';
      row.innerHTML = tags.innerHTML;
      detail.appendChild(row);
    }
    const actions = document.createElement('div');
    actions.className = 'folder-actions';
    if (link) {
      const a = document.createElement('a');
      a.className = 'folder-btn folder-btn-primary';
      a.href = link.href;
      a.target = '_blank';
      a.rel = 'noopener';
      a.textContent = link.textContent.trim();
      a.addEventListener('click', (e) => e.stopPropagation());
      actions.appendChild(a);
    } else if (noLink) {
      const span = document.createElement('span');
      span.className = 'folder-no-link';
      span.textContent = noLink.textContent.trim();
      actions.appendChild(span);
    }
    detail.appendChild(actions);
    folder.appendChild(detail);

    stack.appendChild(folder);
  });

  const folders = Array.from(stack.children);
  const isMobile = () => window.matchMedia('(max-width:860px)').matches;

  /* ---- mobile: plain accordion, no scroll rig ---- */
  function wireMobile() {
    let openIndex = 0;
    folders.forEach((f, i) => {
      f.classList.toggle('is-active', i === openIndex);
      f.onclick = () => {
        openIndex = i;
        folders.forEach((f2, j) => f2.classList.toggle('is-active', j === openIndex));
      };
    });
  }

  /* ---- desktop: scroll gives a subtle ambient "riffle" through the
     collapsed stack (nothing opens on its own); a click is the only
     thing that expands a folder into its full detail card. ---- */
  let hoverIndex = -1;
  let expandedIndex = null;
  const TAB_H = folders[0].querySelector('.folder-tab-row').offsetHeight;
  const TAB_STEP = 54; /* stagger between collapsed tabs, sized for the bigger cards */

  function layout() {
    /* +40vh settle buffer at the end: without it, momentum scroll can carry
       a few pixels past the exact instant position:sticky releases while
       progress is still clamped to 1, leaving the last folder rendered as
       if still pinned even though its container already scrolled away. */
    track.style.height = (150 + n * 20 + 40) + 'vh';
  }

  function scrollFloatIndex() {
    const trackRect = track.getBoundingClientRect();
    /* Subtract the settle buffer so progress reaches 1 a bit before the
       track's true end, leaving slack scroll room where the last folder
       stays fully settled (and the section still pinned) instead of
       sitting exactly on the position:sticky release boundary. */
    const total = trackRect.height - window.innerHeight - window.innerHeight * 0.4;
    const progress = total > 0 ? Math.min(1, Math.max(0, -trackRect.top / total)) : 0;
    return progress * (n - 1);
  }

  function render() {
    const centerIdx = expandedIndex !== null ? expandedIndex : scrollFloatIndex();
    const expandedFolder = expandedIndex !== null ? folders[expandedIndex] : null;
    /* detail's visual max-height caps at min(520px,60vh), so clamp the raw
       scrollHeight to that same cap; otherwise long descriptions would
       reserve more offset for the folders below than the card actually
       occupies on screen, leaving a gap. */
    const detailCapPx = Math.min(520, window.innerHeight * 0.6);
    const expandedH = expandedFolder
      ? TAB_H + Math.min(expandedFolder.querySelector('.folder-detail').scrollHeight, detailCapPx)
      : TAB_H;

    folders.forEach((folder, i) => {
      const isExpanded = i === expandedIndex;
      const offset = i - centerIdx;
      const hovering = i === hoverIndex && !isExpanded && expandedIndex === null;
      let ty, scale, opacity, z;

      if (isExpanded) {
        ty = 0; scale = 1; opacity = 1; z = 200;
      } else if (offset > 0) {
        /* not reached yet: queues up behind the front card, receding into
           the cabinet and fading toward the top, only shrinking a little
           so the far end of the stack still reads as folders, not dots. */
        const k = Math.min(offset, 8);
        ty = -(expandedH + (k - 1) * TAB_STEP) + (hovering ? 8 : 0);
        scale = Math.max(0.8, 1 - 0.025 * k);
        opacity = Math.max(0, 1 - 0.12 * k);
        z = 90 - k;
      } else {
        /* already shown: exits down past the front edge of the drawer. */
        const k = Math.min(-offset, 3);
        ty = k * TAB_STEP * 1.4;
        scale = Math.max(0.85, 1 - 0.05 * k);
        opacity = Math.max(0, 1 - 0.4 * k);
        z = 90 - k;
      }

      folder.style.transform =
        'translateX(-50%) translateY(' + ty + 'px) scale(' + scale + ')';
      folder.style.opacity = String(opacity);
      folder.style.zIndex = String(z);
      folder.classList.toggle('is-active', isExpanded);
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
      folder.addEventListener('click', () => {
        expandedIndex = expandedIndex === i ? null : i;
        render();
      });
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
      folders.forEach((f) => { f.style.transform = ''; f.style.opacity = ''; f.style.zIndex = ''; });
      track.style.height = '';
      if (mobileMode) wireMobile(); else wireDesktop();
    }
  });
})();
