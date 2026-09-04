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
  const MIN_SCALE = 0.8;

  cards.forEach((card, i) => {
    const h3 = card.querySelector('.project-info h3');
    const desc = card.querySelector('.project-info p');
    const tagRow = card.querySelector('.tag-row');
    const link = card.querySelector('.project-links a');
    const noLink = card.querySelector('.no-link');

    const wrap = document.createElement('div');
    wrap.className = 'stack-card-wrap';
    wrap.style.zIndex = String(10 + i);
    wrap.style.setProperty('--stack-top-step', (i * 16) + 'px');

    const el = document.createElement('div');
    el.className = 'stack-card';

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

/* CIRCULAR GALLERY: a 3D ring of award cards built from the hidden
   .awards-data figures (single source of truth). The ring rotates one
   full turn across the track's scroll range, and drifts slowly on its
   own whenever the user isn't actively scrolling. */
(function () {
  const track = document.getElementById('gallery-track');
  const carousel = document.getElementById('gallery-carousel');
  const figures = document.querySelectorAll('.awards-data .award-card');
  if (!track || !carousel || !figures.length) return;

  const n = figures.length;
  const anglePerItem = 360 / n;
  const AUTO_ROTATE_SPEED = 0.03;

  figures.forEach((figure, i) => {
    const img = figure.querySelector('img');
    const year = figure.querySelector('.year');
    const caption = figure.querySelector('figcaption');

    let captionText = '';
    if (caption) {
      const clone = caption.cloneNode(true);
      const y = clone.querySelector('.year');
      if (y) y.remove();
      captionText = clone.textContent.trim();
    }

    const card = document.createElement('div');
    card.className = 'gallery-card';
    card.style.transform = 'rotateY(' + (i * anglePerItem) + 'deg) translateZ(var(--radius))';

    const photo = document.createElement('img');
    photo.src = img.getAttribute('src');
    photo.alt = img.getAttribute('alt') || '';
    photo.loading = 'lazy';
    card.appendChild(photo);

    const scrim = document.createElement('div');
    scrim.className = 'gallery-card-scrim';
    card.appendChild(scrim);

    const cap = document.createElement('div');
    cap.className = 'gallery-card-cap';
    cap.innerHTML =
      (year ? '<span class="year">' + year.textContent.trim() + '</span>' : '') +
      '<p>' + captionText + '</p>';
    card.appendChild(cap);

    carousel.appendChild(card);
  });

  const cards = Array.from(carousel.children);
  let rotation = 0;
  let isScrolling = false;
  let scrollTimeout = null;

  function layout() {
    track.style.height = (100 + n * 40) + 'vh';
  }

  function scrollProgress() {
    const rect = track.getBoundingClientRect();
    const total = rect.height - window.innerHeight;
    return total > 0 ? Math.min(1, Math.max(0, -rect.top / total)) : 0;
  }

  function render() {
    carousel.style.transform = 'rotateY(' + rotation + 'deg)';
    const totalRotation = ((rotation % 360) + 360) % 360;
    cards.forEach((card, i) => {
      const itemAngle = i * anglePerItem;
      const relativeAngle = (itemAngle + totalRotation + 360) % 360;
      const normalizedAngle = relativeAngle > 180 ? 360 - relativeAngle : relativeAngle;
      card.style.opacity = String(Math.max(0.3, 1 - normalizedAngle / 180));
    });
  }

  function onScroll() {
    isScrolling = true;
    if (scrollTimeout) clearTimeout(scrollTimeout);
    rotation = scrollProgress() * 360;
    render();
    scrollTimeout = setTimeout(() => { isScrolling = false; }, 150);
  }

  function tick() {
    if (!isScrolling) {
      rotation += AUTO_ROTATE_SPEED;
      render();
    }
    requestAnimationFrame(tick);
  }

  layout();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', layout);
  render();
  requestAnimationFrame(tick);
})();

/* STACK GRAPH: a force-directed knowledge graph of the real tech stack
   (force-graph, the vanilla engine behind react-force-graph; no React
   needed here). Category nodes ("Languages", "Web & Backend", ...) are
   hubs; every technology is a single node, home-linked to its primary
   category, drawn with its real brand logo (Simple Icons CDN) where
   one exists. A technology actually used across more than one category
   (per the Experience/Selected Work tags and a GitHub/LinkedIn audit,
   not just the Stack list) gets an extra link to that category instead
   of being listed twice, so the physics settle it as a bridge node
   pulled between clusters. No click/scroll zoom: the graph only reacts
   to hovering (link highlight) and cursor position (a subtle 3D tilt). */
(function () {
  if (typeof ForceGraph === 'undefined') return;
  const container = document.getElementById('stack-graph');
  if (!container) return;

  const CATEGORIES = ['Languages', 'Web & Backend', 'AI / LLM', 'Data & Infra', 'Embedded & IoT', 'Other'];

  /* [name, home category, extra categories it also bridges to, Simple Icons slug or null] */
  const TECH = [
    ['Python', 'Languages', ['AI / LLM', 'Data & Infra', 'Embedded & IoT', 'Other'], 'python'],
    ['C++', 'Languages', ['Embedded & IoT'], 'cplusplus'],
    ['TypeScript', 'Languages', ['Web & Backend'], 'typescript'],
    ['JavaScript', 'Languages', [], 'javascript'],
    ['SQL', 'Languages', ['Data & Infra'], null],

    ['React', 'Web & Backend', [], 'react'],
    ['Node.js', 'Web & Backend', [], 'nodedotjs'],
    ['Express', 'Web & Backend', [], 'express'],
    ['Prisma', 'Web & Backend', [], 'prisma'],
    ['Sequelize', 'Web & Backend', [], 'sequelize'],
    ['REST APIs', 'Web & Backend', [], null],
    ['Socket.IO', 'Web & Backend', [], 'socketdotio'],
    ['Telegram API', 'Web & Backend', ['AI / LLM'], 'telegram'],
    ['Playwright', 'Web & Backend', ['AI / LLM'], 'playwright'],

    ['Gemini', 'AI / LLM', [], 'googlegemini'],
    ['RAG', 'AI / LLM', ['Web & Backend'], null],
    ['Prompt-Injection Defense', 'AI / LLM', [], null],
    ['Langfuse', 'AI / LLM', [], null],
    ['OCR', 'AI / LLM', [], null],
    ['Speech-to-Text', 'AI / LLM', [], null],
    ['Claude Code', 'AI / LLM', [], 'claude'],
    ['Multi-LLM', 'AI / LLM', [], null],
    ['PyTorch', 'AI / LLM', [], 'pytorch'],
    ['LoRA', 'AI / LLM', [], null],
    ['NLP', 'AI / LLM', [], null],

    ['PostgreSQL', 'Data & Infra', ['Web & Backend'], 'postgresql'],
    ['MySQL', 'Data & Infra', ['Web & Backend'], 'mysql'],
    ['Redis', 'Data & Infra', [], 'redis'],
    ['Docker', 'Data & Infra', ['Web & Backend'], 'docker'],
    ['HL7/FHIR/DICOM', 'Data & Infra', [], null],
    ['Sentry', 'Data & Infra', [], 'sentry'],
    ['Cron', 'Data & Infra', ['AI / LLM'], null],
    ['ETL', 'Data & Infra', [], null],

    ['ESP32', 'Embedded & IoT', [], 'espressif'],
    ['STM32', 'Embedded & IoT', [], 'stmicroelectronics'],
    ['Arduino', 'Embedded & IoT', [], 'arduino'],
    ['FreeRTOS', 'Embedded & IoT', [], null],
    ['LoRaWAN', 'Embedded & IoT', [], null],
    ['Raspberry Pi', 'Embedded & IoT', [], 'raspberrypi'],
    ['LoRa (SX1278)', 'Embedded & IoT', [], null],
    ['GPS', 'Embedded & IoT', [], null],
    ['ThingSpeak', 'Embedded & IoT', [], null],

    ['DSA', 'Other', [], null],
    ['Competitive Programming', 'Other', [], null],
    ['Blockchain Fundamentals', 'Other', [], null],
    ['PyBullet', 'Other', [], null],
    ['A*/RRT*', 'Other', [], null],
    ['PID Control', 'Other', [], null],
    ['pytest', 'Other', ['AI / LLM'], 'pytest'],
  ];

  const root = getComputedStyle(document.documentElement);
  const GOLD = root.getPropertyValue('--gold').trim() || '#c9a227';
  const INK = root.getPropertyValue('--ink').trim() || '#f5f5f7';
  const SANS = root.getPropertyValue('--sans').trim() || 'sans-serif';

  function hexToRgba(hex, a) {
    const h = hex.replace('#', '');
    const r = parseInt(h.substring(0, 2), 16);
    const g = parseInt(h.substring(2, 4), 16);
    const b = parseInt(h.substring(4, 6), 16);
    return 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')';
  }

  /* fallback color for nodes with no brand logo (a technique/concept,
     not a product), tinted by their home category so the graph still
     reads as colorful and organized rather than falling back to gray */
  const CATEGORY_FALLBACK = {
    'Languages': '#e0c168',
    'Web & Backend': '#5b9dd9',
    'AI / LLM': '#c084e8',
    'Data & Infra': '#57c2a8',
    'Embedded & IoT': '#e8934a',
    'Other': '#9aa5b7',
  };

  const HUB_R = 24;
  const TECH_R = 17;

  /* an ellipse, not a circle: the box is landscape, so spreading hubs
     wider than they are tall uses more of it before zoomToFit scales in */
  const hubAngle = (cat) => CATEGORIES.indexOf(cat) * (2 * Math.PI / CATEGORIES.length);
  const hubX = (cat) => 230 * Math.cos(hubAngle(cat));
  const hubY = (cat) => 150 * Math.sin(hubAngle(cat));

  const nodes = CATEGORIES.map((cat) => (
    { id: cat, type: 'category', r: HUB_R, x: hubX(cat), y: hubY(cat) }
  ));
  const links = [];
  const logoCache = {};
  TECH.forEach(([name, home, extras, slug]) => {
    /* every tech node also starts already spread toward its home hub
       (not at d3-force's default near-origin spawn point), so the graph
       looks right immediately rather than depending on how many physics
       ticks actually run before the layout is considered "settled" */
    const jitterX = (Math.random() - 0.5) * 60;
    const jitterY = (Math.random() - 0.5) * 60;
    nodes.push({
      id: name, type: 'tech', home, r: TECH_R, color: CATEGORY_FALLBACK[home],
      x: hubX(home) * 0.6 + jitterX, y: hubY(home) * 0.6 + jitterY,
    });
    links.push({ source: name, target: home });
    extras.forEach((cat) => links.push({ source: name, target: cat }));
    if (slug && !logoCache[slug]) {
      const img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = () => Graph.nodeColor(Graph.nodeColor());
      img.src = 'https://cdn.simpleicons.org/' + slug;
      logoCache[slug] = img;
    }
  });
  TECH.forEach(([name, , , slug]) => {
    if (slug) nodes.find((n) => n.id === name).logo = logoCache[slug];
  });

  const linksByNode = {};
  nodes.forEach((n) => { linksByNode[n.id] = []; });
  links.forEach((l) => {
    linksByNode[l.source].push(l);
    linksByNode[l.target].push(l);
  });

  const highlightNodes = new Set();
  const highlightLinks = new Set();

  const Graph = ForceGraph()(container)
    .graphData({ nodes, links })
    .backgroundColor('rgba(0,0,0,0)')
    .width(container.clientWidth)
    .height(container.clientHeight)
    .enableZoomPanInteraction(false)
    .linkColor((l) => (highlightLinks.has(l) ? 'rgba(201,162,39,.9)' : 'rgba(255,255,255,.14)'))
    .linkWidth((l) => (highlightLinks.has(l) ? 2.5 : 1))
    .nodeCanvasObject((node, ctx, globalScale) => {
      const isCategory = node.type === 'category';
      const isHighlighted = highlightNodes.has(node);
      const dim = !isCategory && highlightNodes.size && !isHighlighted;
      const r = node.r;
      const tint = isCategory ? GOLD : node.color;

      ctx.globalAlpha = dim ? 0.35 : 1;

      /* glass base: soft ambient shadow, then a tinted radial "frosted
         glass" fill (bright near the top-left, fading toward the rim) */
      ctx.save();
      ctx.shadowColor = 'rgba(0,0,0,.55)';
      ctx.shadowBlur = 14;
      ctx.shadowOffsetY = 4;
      ctx.beginPath();
      ctx.arc(node.x, node.y, r, 0, 2 * Math.PI);
      const glass = ctx.createRadialGradient(
        node.x - r * 0.35, node.y - r * 0.35, r * 0.1,
        node.x, node.y, r
      );
      glass.addColorStop(0, hexToRgba(tint, 0.55));
      glass.addColorStop(0.65, hexToRgba(tint, 0.3));
      glass.addColorStop(1, hexToRgba(tint, 0.16));
      ctx.fillStyle = glass;
      ctx.fill();
      ctx.restore();

      /* glass edge: a bright, thin rim */
      ctx.lineWidth = isCategory ? 1.6 : 1.1;
      ctx.strokeStyle = isHighlighted ? 'rgba(255,255,255,.8)' : 'rgba(255,255,255,.4)';
      ctx.stroke();

      /* glossy highlight crescent, top-left */
      ctx.beginPath();
      ctx.arc(node.x - r * 0.32, node.y - r * 0.35, r * 0.38, 0, 2 * Math.PI);
      ctx.fillStyle = 'rgba(255,255,255,.22)';
      ctx.fill();

      if (node.logo && node.logo.complete && node.logo.naturalWidth > 0) {
        /* a bright backing disc makes any-color logo pop off the tinted
           glass, plus its own small shadow to lift it off the surface */
        ctx.save();
        ctx.shadowColor = 'rgba(0,0,0,.4)';
        ctx.shadowBlur = 5;
        ctx.beginPath();
        ctx.arc(node.x, node.y, r * 0.68, 0, 2 * Math.PI);
        ctx.fillStyle = 'rgba(248,248,250,.94)';
        ctx.fill();
        ctx.restore();

        const s = r * 1.15;
        ctx.save();
        ctx.beginPath();
        ctx.arc(node.x, node.y, r * 0.68, 0, 2 * Math.PI);
        ctx.clip();
        ctx.drawImage(node.logo, node.x - s / 2, node.y - s / 2, s, s);
        ctx.restore();
      }

      if (isCategory || isHighlighted || globalScale > 1.6) {
        const fontSize = (isCategory ? 14 : 11) / globalScale;
        ctx.font = (isCategory ? '700 ' : '600 ') + fontSize + 'px ' + SANS;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        ctx.fillStyle = isCategory ? INK : 'rgba(255,255,255,.9)';
        ctx.fillText(node.id, node.x, node.y + r + 3);
      }
      ctx.globalAlpha = 1;
    })
    .nodePointerAreaPaint((node, color, ctx) => {
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(node.x, node.y, node.r + 4, 0, 2 * Math.PI);
      ctx.fill();
    })
    .onNodeHover((node) => {
      highlightNodes.clear();
      highlightLinks.clear();
      if (node) {
        highlightNodes.add(node);
        linksByNode[node.id].forEach((l) => {
          highlightLinks.add(l);
          highlightNodes.add(l.source === node ? l.target : l.source);
        });
      }
      container.style.cursor = node ? 'pointer' : 'grab';
      Graph.nodeColor(Graph.nodeColor()).linkColor(Graph.linkColor()).linkWidth(Graph.linkWidth());
    })
    .onEngineTick(() => {
      /* hard-clamp every node to a fixed radius from the origin so the
         layout can never drift past the container's edge, no matter how
         the charge/link forces settle or a drag reheats the simulation */
      const MAX_R = 270;
      nodes.forEach((n) => {
        const d = Math.sqrt(n.x * n.x + n.y * n.y);
        if (d > MAX_R) {
          const k = MAX_R / d;
          n.x *= k;
          n.y *= k;
        }
      });

      /* manual collision pass: push any pair of circles apart so nodes
         never render overlapping, regardless of how charge/link settle */
      const GAP = 4;
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const a = nodes[i], b = nodes[j];
          const dx = b.x - a.x, dy = b.y - a.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          const minDist = a.r + b.r + GAP;
          if (dist > 0 && dist < minDist) {
            const push = (minDist - dist) / 2;
            const ux = dx / dist, uy = dy / dist;
            a.x -= ux * push; a.y -= uy * push;
            b.x += ux * push; b.y += uy * push;
          } else if (dist === 0) {
            a.x -= 0.5; b.x += 0.5;
          }
        }
      }
    })
    .onEngineStop(() => Graph.zoomToFit(400, 55));

  Graph.d3Force('charge').strength(-200);
  Graph.d3Force('link').distance(78);

  /* fit to the (now-reasonable) initial layout right away, then again
     a couple of times as the physics settle: onEngineStop alone can fire
     earlier than expected when the page is busy elsewhere (scroll
     animations, the WebGL background), so this doesn't depend on it */
  Graph.zoomToFit(0, 55);
  setTimeout(() => Graph.zoomToFit(300, 55), 400);
  setTimeout(() => Graph.zoomToFit(300, 55), 1600);

  window.addEventListener('resize', () => {
    Graph.width(container.clientWidth).height(container.clientHeight);
  });

  /* subtle 3D tilt that follows the cursor instead of a zoom control */
  const MAX_TILT = 6;
  container.style.transition = 'transform .5s ease-out';
  container.addEventListener('mousemove', (e) => {
    const rect = container.getBoundingClientRect();
    const px = (e.clientX - rect.left) / rect.width - 0.5;
    const py = (e.clientY - rect.top) / rect.height - 0.5;
    container.style.transition = 'transform .1s linear';
    container.style.transform =
      'perspective(1400px) rotateX(' + (-py * MAX_TILT) + 'deg) rotateY(' + (px * MAX_TILT) + 'deg)';
  });
  container.addEventListener('mouseleave', () => {
    container.style.transition = 'transform .5s ease-out';
    container.style.transform = 'perspective(1400px) rotateX(0deg) rotateY(0deg)';
  });
})();

/* BUILD ACTIVITY CHART: a small smoothed multi-series area chart drawn
   straight into the inline SVG, no charting library. Data is real GitHub
   commit counts (Aug 29 - Sep 4, 2026) pulled once via `gh api` across
   the actively-developed repos, not a live-fetched dashboard. */
(function () {
  const svg = document.getElementById('activity-chart');
  if (!svg) return;

  const SERIES = [
    { hex: '#c9a227', data: [5, 0, 0, 0, 0, 0, 0] },   /* Livora */
    { hex: '#57c2a8', data: [0, 0, 0, 0, 0, 14, 10] }, /* Second Brain */
    { hex: '#c084e8', data: [0, 0, 0, 0, 6, 11, 27] }, /* Portfolio */
  ];
  const N = 7;
  const W = 320, PAD_X = 8, TOP = 8, BASE = 112, MAX = 30;
  const stepX = (W - PAD_X * 2) / (N - 1);
  const x = (i) => PAD_X + i * stepX;
  const y = (v) => BASE - (v / MAX) * (BASE - TOP);

  function smoothPath(points) {
    let d = 'M ' + points[0][0] + ',' + points[0][1];
    for (let i = 0; i < points.length - 1; i++) {
      const mx = (points[i][0] + points[i + 1][0]) / 2;
      const my = (points[i][1] + points[i + 1][1]) / 2;
      d += ' Q ' + points[i][0] + ',' + points[i][1] + ' ' + mx + ',' + my;
    }
    const last = points[points.length - 1];
    d += ' T ' + last[0] + ',' + last[1];
    return d;
  }

  const NS = 'http://www.w3.org/2000/svg';
  const defs = document.createElementNS(NS, 'defs');
  svg.appendChild(defs);

  SERIES.forEach((s, i) => {
    const points = s.data.map((v, j) => [x(j), y(v)]);
    const top = smoothPath(points);

    const gradId = 'activity-grad-' + i;
    const grad = document.createElementNS(NS, 'linearGradient');
    grad.setAttribute('id', gradId);
    grad.setAttribute('x1', '0'); grad.setAttribute('y1', '0');
    grad.setAttribute('x2', '0'); grad.setAttribute('y2', '1');
    const stopTop = document.createElementNS(NS, 'stop');
    stopTop.setAttribute('offset', '0%'); stopTop.setAttribute('stop-color', s.hex); stopTop.setAttribute('stop-opacity', '0.35');
    const stopBottom = document.createElementNS(NS, 'stop');
    stopBottom.setAttribute('offset', '100%'); stopBottom.setAttribute('stop-color', s.hex); stopBottom.setAttribute('stop-opacity', '0');
    grad.appendChild(stopTop); grad.appendChild(stopBottom);
    defs.appendChild(grad);

    const area = document.createElementNS(NS, 'path');
    area.setAttribute('d', top + ' L ' + x(N - 1) + ',' + BASE + ' L ' + x(0) + ',' + BASE + ' Z');
    area.setAttribute('fill', 'url(#' + gradId + ')');
    svg.appendChild(area);

    const line = document.createElementNS(NS, 'path');
    line.setAttribute('d', top);
    line.setAttribute('fill', 'none');
    line.setAttribute('stroke', s.hex);
    line.setAttribute('stroke-width', '2');
    line.setAttribute('stroke-linecap', 'round');
    svg.appendChild(line);
  });
})();
