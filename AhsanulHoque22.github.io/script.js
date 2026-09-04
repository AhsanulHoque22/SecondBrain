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
      .to('[data-parallax-layer="4"]', { yPercent: -15, ease: 'none' }, 0) /* role title */
      /* sharp at rest; only picks up a blurred edge once you scroll (see
         .hero-photo-blur's radial mask, which keeps the center sharp). */
      .to('.hero-photo-blur', { '--edge-blur': 14, ease: 'none' }, 0);
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

/* ---------- Site background: WebGL topographic contour field ----------
   Adapted from a supplied React component (a shared effects file wrapping
   this shader in a sandboxed iframe with React props/state/light-dark
   theming). All of that machinery exists only to make the effect reusable
   as a packaged component across a design system; this site has one
   canvas in one place, so the shader runs directly against it with no
   iframe, no React, no build step, no new dependency, only the vertex/
   fragment shaders and the render loop that actually draw the effect.
   Replaces the old 2D particle-constellation canvas as the site's single
   fixed full-page background, rather than running both at once. */
(function () {
  const canvas = document.getElementById('topo-canvas');
  if (!canvas) return;
  const gl = canvas.getContext('webgl', { alpha: false, antialias: false, depth: false });
  if (!gl) return; /* no WebGL: the page's plain black background shows instead */

  const vsSource = `
    attribute vec2 a_position;
    void main() { gl_Position = vec4(a_position, 0.0, 1.0); }
  `;
  const fsSource = `
    precision highp float;
    uniform vec2 u_resolution;
    uniform float u_time;
    uniform float u_dpr;

    vec3 permute(vec3 x) { return mod(((x*34.0)+1.0)*x, 289.0); }
    float snoise(vec2 v){
      const vec4 C = vec4(0.211324865405187, 0.366025403784439, -0.577350269189626, 0.024390243902439);
      vec2 i  = floor(v + dot(v, C.yy) );
      vec2 x0 = v -   i + dot(i, C.xx);
      vec2 i1; i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
      vec4 x12 = x0.xyxy + C.xxzz; x12.xy -= i1;
      i = mod(i, 289.0);
      vec3 p = permute( permute( i.y + vec3(0.0, i1.y, 1.0 )) + i.x + vec3(0.0, i1.x, 1.0 ));
      vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy), dot(x12.zw,x12.zw)), 0.0);
      m = m*m; m = m*m;
      vec3 x = 2.0 * fract(p * C.www) - 1.0;
      vec3 h = abs(x) - 0.5; vec3 ox = floor(x + 0.5);
      vec3 a0 = x - ox; m *= 1.79284291400159 - 0.85373472095314 * ( a0*a0 + h*h );
      vec3 g; g.x  = a0.x  * x0.x  + h.x  * x0.y; g.yz = a0.yz * x12.xz + h.yz * x12.yw;
      return 130.0 * dot(m, g);
    }

    void main() {
      vec2 st = gl_FragCoord.xy / u_resolution.xy;
      st.x *= u_resolution.x / u_resolution.y;

      /* 1px physical grid */
      float gridSize = 48.0 * u_dpr;
      vec2 gridSt = gl_FragCoord.xy / gridSize;
      vec2 gridFract = fract(gridSt);
      float lineThickness = 1.0 / gridSize;
      float gridLines = step(1.0 - lineThickness, gridFract.x) + step(1.0 - lineThickness, gridFract.y);
      gridLines = clamp(gridLines, 0.0, 1.0) * 0.12;

      /* ultra-thin topographic contour lines from 2D simplex noise */
      float noiseScale = 1.4;
      vec2 noisePos = st * noiseScale + vec2(u_time * 0.015, u_time * 0.025);
      float n = snoise(noisePos) * 0.5 + 0.5;
      float numBands = 10.0;
      float bandVal = n * numBands;
      float triangleWave = abs(fract(bandVal) - 0.5) * 2.0;
      float topoLines = smoothstep(0.02, 0.00, triangleWave) * 0.45;

      vec3 color = vec3(0.0);
      color += vec3(1.0) * gridLines;
      color += vec3(1.0) * topoLines;

      gl_FragColor = vec4(color, 1.0);
    }
  `;

  function createShader(type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    return shader;
  }

  const program = gl.createProgram();
  gl.attachShader(program, createShader(gl.VERTEX_SHADER, vsSource));
  gl.attachShader(program, createShader(gl.FRAGMENT_SHADER, fsSource));
  gl.linkProgram(program);
  gl.useProgram(program);

  const positionBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  const positionLocation = gl.getAttribLocation(program, 'a_position');
  gl.enableVertexAttribArray(positionLocation);
  gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

  const resolutionLocation = gl.getUniformLocation(program, 'u_resolution');
  const timeLocation = gl.getUniformLocation(program, 'u_time');
  const dprLocation = gl.getUniformLocation(program, 'u_dpr');

  function resizeTopo() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(window.innerWidth * dpr);
    canvas.height = Math.round(window.innerHeight * dpr);
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.uniform2f(resolutionLocation, canvas.width, canvas.height);
    gl.uniform1f(dprLocation, dpr);
  }
  window.addEventListener('resize', resizeTopo);
  resizeTopo();

  const startTime = performance.now();
  function renderTopo(time) {
    gl.uniform1f(timeLocation, (time - startTime) * 0.001);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    requestAnimationFrame(renderTopo);
  }
  requestAnimationFrame(renderTopo);
})();

/* STICKY STACK: cards are built once from the hidden .project-data
   cards (single source of truth), then pin to the viewport top in
   sequence. A single scrub timeline scales each card down over an
   increasing share of the section's scroll range, so earlier cards
   settle smaller as later ones stack on top of them. Clicking a card
   navigates straight to its project link. */
(function () {
  const track = document.getElementById('stack-track');
  const cards = document.querySelectorAll('.project-data .project-card');
  if (!track || !cards.length) return;

  const n = cards.length;
  const ACCENTS = ['var(--cyan)', 'var(--violet)', 'var(--gold)'];
  const MIN_SCALE = 0.8;

  cards.forEach((card, i) => {
    const h3 = card.querySelector('.project-info h3');
    const img = card.querySelector('.project-poster');
    const desc = card.querySelector('.project-info p');
    const tagRow = card.querySelector('.tag-row');
    const link = card.querySelector('.project-links a');
    const noLink = card.querySelector('.no-link');

    const wrap = document.createElement('div');
    wrap.className = 'stack-card-wrap';
    wrap.style.zIndex = String(10 + i);
    wrap.style.setProperty('--stack-top-step', (i * 16) + 'px');

    const el = document.createElement('div');
    el.className = 'stack-card' + (img ? '' : ' no-image');
    el.style.setProperty('--accent', ACCENTS[i % ACCENTS.length]);

    if (img) {
      const bg = document.createElement('img');
      bg.className = 'stack-card-img';
      bg.src = img.getAttribute('src');
      bg.alt = img.getAttribute('alt') || '';
      bg.loading = 'lazy';
      el.appendChild(bg);
      const scrim = document.createElement('div');
      scrim.className = 'stack-card-scrim';
      el.appendChild(scrim);
    }

    const num = document.createElement('div');
    num.className = 'stack-card-num';
    num.textContent = String(i + 1).padStart(2, '0');
    el.appendChild(num);

    const body = document.createElement('div');
    body.className = 'stack-card-body';
    body.innerHTML =
      '<h3>' + (h3 ? h3.innerHTML : '') + '</h3>' +
      '<p>' + (desc ? desc.textContent.trim() : '') + '</p>' +
      '<div class="stack-card-foot">' +
        (tagRow ? tagRow.outerHTML : '') +
        (link ? '<span class="stack-card-link">' + link.textContent.trim() + '</span>' : (noLink ? noLink.outerHTML : '')) +
      '</div>';
    el.appendChild(body);

    if (link) {
      el.addEventListener('click', () => window.open(link.href, '_blank', 'noopener'));
    } else {
      el.style.cursor = 'default';
    }

    wrap.appendChild(el);
    track.appendChild(wrap);
  });

  const els = Array.from(track.children).map((wrap) => wrap.firstElementChild);

  const tl = gsap.timeline({
    scrollTrigger: { trigger: track, start: 'top top', end: 'bottom bottom', scrub: 0.3 },
  });
  els.forEach((el, i) => {
    if (i === n - 1) return; /* last card sits on top, never shrinks */
    const targetScale = MIN_SCALE + (1 - MIN_SCALE) * (i / (n - 1));
    const start = i / n;
    tl.to(el, { scale: targetScale, ease: 'none', duration: 1 - start }, start);
  });
})();
