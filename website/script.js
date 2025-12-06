// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add scroll animation effects
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all sections for animation
document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });

    // Animate stat cards on scroll
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        card.style.transitionDelay = `${index * 0.1}s`;
    });

    // Animate testimonial cards
    const testimonialCards = document.querySelectorAll('.testimonial-card');
    testimonialCards.forEach((card, index) => {
        card.style.transitionDelay = `${index * 0.15}s`;
    });
});

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.style.transform = `translateY(${scrolled * 0.3}px)`;
    }
});

// Add hover effect to insight cards
const insightCards = document.querySelectorAll('.insight-card');
insightCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.borderColor = 'var(--accent-green)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.borderColor = 'var(--border-color)';
    });
});

// Continuous scroll for testimonials (placeholder for future implementation)
function initTestimonialScroll() {
    const testimonialsGrid = document.querySelector('.testimonials-grid');
    if (testimonialsGrid) {
        // This will be implemented when we have actual testimonial data
        // For now, it's a placeholder for the continuous scroll feature
        console.log('Testimonial scroll initialized');
    }
}

initTestimonialScroll();

// Button click handlers
document.addEventListener('DOMContentLoaded', () => {
    const authBtn = document.querySelector('.btn-auth');
    if (authBtn) {
        authBtn.addEventListener('click', () => {
            alert('Login/Signup functionality will be implemented');
        });
    }

    const discoverBtn = document.querySelector('.skills-section .btn-primary');
    if (discoverBtn) {
        discoverBtn.addEventListener('click', () => {
            window.location.href = 'job-discovery.html';
        });
    }

    const marketBtn = document.querySelector('.btn-secondary');
    if (marketBtn) {
        marketBtn.addEventListener('click', () => {
            window.location.href = 'market-analysis.html';
        });
    }

    const reviewBtn = document.querySelector('.feedback-section .btn-primary');
    if (reviewBtn) {
        reviewBtn.addEventListener('click', () => {
            alert('Review form will be implemented');
        });
    }
});

// Add dynamic grid animation
function createGridAnimation() {
    const body = document.body;
    let mouseX = 0;
    let mouseY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // This creates a subtle interactive effect with the grid
    setInterval(() => {
        const gridOffset = Math.sin(Date.now() / 1000) * 2;
        body.style.backgroundPosition = `${gridOffset}px ${gridOffset}px`;
    }, 50);
}

createGridAnimation();
