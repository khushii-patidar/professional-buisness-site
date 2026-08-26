'use strict';

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// ── SCROLL PROGRESS BAR ────────────────────────────────────────────────────────
const progressBar = document.getElementById('scrollProgress');
if (progressBar) {
  const updateProgress = () => {
    const h = document.documentElement;
    const scrolled = h.scrollTop;
    const max = h.scrollHeight - h.clientHeight;
    progressBar.style.width = (max > 0 ? (scrolled / max) * 100 : 0) + '%';
  };
  window.addEventListener('scroll', updateProgress, { passive: true });
  updateProgress();
}

// ── NAVBAR SCROLL & BACK TO TOP ───────────────────────────────────────────────
const nav = document.getElementById('mainNav');
const backToTopBtn = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;
  if (nav) {
    nav.classList.toggle('scrolled', scrollY > 40);
  }
  if (backToTopBtn) {
    if (scrollY > 400) {
      backToTopBtn.classList.add('show');
    } else {
      backToTopBtn.classList.remove('show');
    }
  }
}, { passive: true });

if (backToTopBtn) {
  backToTopBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ── ACTIVE NAV HIGHLIGHT ──────────────────────────────────────────────────────
const path = window.location.pathname;
document.querySelectorAll('.nav-link').forEach(link => {
  const href = link.getAttribute('href');
  if (href && (path === href || (href !== '/' && path.startsWith(href)))) {
    link.classList.add('active');
  }
});

// ── SMOOTH SCROLL FOR ANCHOR LINKS ───────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const targetId = this.getAttribute('href');
    if (targetId && targetId !== '#') {
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const offset = nav ? nav.offsetHeight + 16 : 80;
        window.scrollTo({
          top: target.getBoundingClientRect().top + window.scrollY - offset,
          behavior: 'smooth'
        });
        const menu = document.getElementById('navMenu');
        if (menu && menu.classList.contains('show')) {
          document.querySelector('.navbar-toggler')?.click();
        }
      }
    }
  });
});

// ── INTERSECTION OBSERVER (AOS ANIMATIONS) ───────────────────────────────────
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const delay = parseInt(entry.target.dataset.aosDelay || 0);
      setTimeout(() => entry.target.classList.add('aos-animate'), delay);
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('[data-aos]').forEach(el => observer.observe(el));

// ── COUNTER ANIMATION ─────────────────────────────────────────────────────────
const countObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const el = entry.target;
    const fullText = el.textContent.trim();
    
    // Check if format is like 5.0★
    if (fullText.includes('.')) {
      const match = fullText.match(/^([\d.]+)(.*)$/);
      if (match) {
        const targetNum = parseFloat(match[1]);
        const suffix = match[2];
        const start = performance.now();
        const dur = 1400;
        const tick = (now) => {
          const p = Math.min((now - start) / dur, 1);
          const e = 1 - Math.pow(1 - p, 3);
          el.textContent = (e * targetNum).toFixed(1) + suffix;
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      }
      countObserver.unobserve(el);
      return;
    }
    
    const num = parseInt(fullText.replace(/\D/g, ''));
    const suffix = fullText.replace(/[\d]/g, '');
    if (!isNaN(num) && num > 0) {
      const start = performance.now();
      const dur = 1600;
      const tick = (now) => {
        const p = Math.min((now - start) / dur, 1);
        const e = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.floor(e * num) + suffix;
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }
    countObserver.unobserve(el);
  });
}, { threshold: 0.4 });

document.querySelectorAll('.stat-num, .about-mini-num').forEach(el => countObserver.observe(el));

// ── MULTI-COLOR NEON PARTICLES ────────────────────────────────────────────────
const container = document.getElementById('particles');
if (container && !prefersReducedMotion) {
  const colors = [
    'rgba(165, 180, 252, 0.7)',
    'rgba(56, 189, 248, 0.7)',
    'rgba(192, 132, 252, 0.7)',
    'rgba(244, 114, 182, 0.6)'
  ];
  for (let i = 0; i < 28; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const size = 2 + Math.random() * 3.5;
    const color = colors[Math.floor(Math.random() * colors.length)];
    p.style.cssText = `
      left: ${Math.random() * 100}%;
      top: ${100 + Math.random() * 20}%;
      width: ${size}px;
      height: ${size}px;
      background: ${color};
      box-shadow: 0 0 10px ${color};
      animation-delay: ${Math.random() * 8}s;
      animation-duration: ${7 + Math.random() * 9}s;
    `;
    container.appendChild(p);
  }
}

