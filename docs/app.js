document.addEventListener("DOMContentLoaded", () => {

    // ---- Scroll Reveal ----
    const revealEls = document.querySelectorAll('.card, .arch-tier, .pipe-step, .agent-row, .file-row, .step-row, .tech-item');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, i) => {
            if (entry.isIntersecting) {
                // Stagger siblings slightly
                const parent = entry.target.parentElement;
                const siblings = Array.from(parent.children).filter(el => revealEls.length > 0);
                const idx = siblings.indexOf(entry.target);
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, Math.max(0, idx * 60));
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    revealEls.forEach(el => observer.observe(el));


    // ---- Navbar shrink ----
    const navbar = document.getElementById('navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;
        if (scrollY > 80) {
            navbar.style.borderBottomColor = 'var(--border)';
        } else {
            navbar.style.borderBottomColor = 'var(--border-light)';
        }
        lastScroll = scrollY;
    }, { passive: true });


    // ---- Mobile nav toggle ----
    const navToggle = document.getElementById('nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('open');
        });

        // Close on link click
        navLinks.querySelectorAll('a').forEach(a => {
            a.addEventListener('click', () => {
                navLinks.classList.remove('open');
            });
        });
    }


    // ---- Smooth scroll ----
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const navHeight = navbar.offsetHeight;
                const top = target.getBoundingClientRect().top + window.pageYOffset - navHeight - 20;
                window.scrollTo({ top, behavior: 'smooth' });
            }
        });
    });

});
