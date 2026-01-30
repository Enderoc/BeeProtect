document.addEventListener('DOMContentLoaded', function () {

    // Fade-in animation
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

    // Navigation active state
    const path = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === path) {
            link.classList.add('active');
        }
    });

    // Stats animation (only numbers)
    document.querySelectorAll('[data-target]').forEach(el => {
        const target = parseInt(el.dataset.target);
        let current = 0;
        const step = Math.max(1, target / 40);

        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                el.textContent = target + (el.dataset.suffix || '');
                clearInterval(timer);
            } else {
                el.textContent = Math.round(current);
            }
        }, 40);
    });

});
