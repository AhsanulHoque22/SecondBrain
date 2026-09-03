gsap.registerPlugin(ScrollTrigger);

/* ---------- Lenis smooth scroll wired to GSAP ticker ---------- */
const lenis = new Lenis({ duration: 1.1, smoothWheel: true });
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);

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
document.querySelectorAll('.project-card').forEach((card) => {
  card.addEventListener('mousemove', (e) => {
    const r = card.getBoundingClientRect();
    const x = ((e.clientX - r.left) / r.width - 0.5) * 6;
    gsap.to(card, { rotateX: -x * 0.3, rotateY: x, duration: 0.4, transformPerspective: 800 });
  });
  card.addEventListener('mouseleave', () => gsap.to(card, { rotateX: 0, rotateY: 0, duration: 0.6 }));
});

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
let w, h, particles;
const mouse = { x: -9999, y: -9999 };

function resize() {
  w = canvas.width = window.innerWidth;
  h = canvas.height = window.innerHeight;
  const count = Math.min(90, Math.floor((w * h) / 18000));
  particles = Array.from({ length: count }, () => ({
    x: Math.random() * w,
    y: Math.random() * h,
    vx: (Math.random() - 0.5) * 0.3,
    vy: (Math.random() - 0.5) * 0.3,
  }));
}
window.addEventListener('resize', resize);
window.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });
resize();

function tick() {
  ctx.clearRect(0, 0, w, h);
  for (const p of particles) {
    p.x += p.vx; p.y += p.vy;
    if (p.x < 0 || p.x > w) p.vx *= -1;
    if (p.y < 0 || p.y > h) p.vy *= -1;
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
