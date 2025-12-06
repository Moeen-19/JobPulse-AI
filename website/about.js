// About Us Page Interactions

document.addEventListener('DOMContentLoaded', () => {
    initTeamCardFlip();
    initScrollAnimations();
    initContactForm();
    initTechStackAnimations();
});

// Team Card Flip Functionality
function initTeamCardFlip() {
    const flipButtons = document.querySelectorAll('.btn-flip');
    
    flipButtons.forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.team-card');
            card.classList.toggle('flipped');
        });
    });
}

// Scroll Animations
function initScrollAnimations() {
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

    // Observe sections
    const sections = document.querySelectorAll('.mission-section, .team-section, .tech-stack-section, .architecture-section, .opensource-section, .contact-section');
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });

    // Animate team cards
    const teamCards = document.querySelectorAll('.team-card');
    teamCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.2}s, transform 0.6s ease ${index * 0.2}s`;
        observer.observe(card);
    });

    // Animate tech categories
    const techCategories = document.querySelectorAll('.tech-category');
    techCategories.forEach((category, index) => {
        category.style.opacity = '0';
        category.style.transform = 'translateY(30px)';
        category.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(category);
    });
}

// Tech Stack Animations
function initTechStackAnimations() {
    const techItems = document.querySelectorAll('.tech-item');
    
    techItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            const logo = this.querySelector('.tech-logo');
            logo.style.transform = 'rotate(360deg)';
            logo.style.transition = 'transform 0.6s ease';
        });
        
        item.addEventListener('mouseleave', function() {
            const logo = this.querySelector('.tech-logo');
            logo.style.transform = 'rotate(0deg)';
        });
    });

    // Animate architecture boxes
    const archBoxes = document.querySelectorAll('.arch-box');
    archBoxes.forEach((box, index) => {
        setTimeout(() => {
            box.style.opacity = '0';
            box.style.transform = 'scale(0.8)';
            box.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            
            setTimeout(() => {
                box.style.opacity = '1';
                box.style.transform = 'scale(1)';
            }, 100);
        }, index * 100);
    });
}

// Contact Form Handling
function initContactForm() {
    const form = document.querySelector('.contact-form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = {
                name: form.querySelector('input[type="text"]').value,
                email: form.querySelector('input[type="email"]').value,
                message: form.querySelector('textarea').value
            };
            
            // In production, send to backend
            console.log('Form submitted:', data);
            
            // Show success message
            showSuccessMessage();
            
            // Reset form
            form.reset();
        });
    }
}

// Show success message
function showSuccessMessage() {
    const message = document.createElement('div');
    message.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: var(--accent-green);
        color: var(--bg-dark);
        padding: 1rem 2rem;
        border-radius: 4px;
        font-weight: 600;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    message.textContent = '✓ Message sent successfully!';
    
    document.body.appendChild(message);
    
    setTimeout(() => {
        message.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            message.remove();
        }, 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Social link interactions
const socialLinks = document.querySelectorAll('.social-link');
socialLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const platform = this.getAttribute('title');
        console.log(`Opening ${platform} profile...`);
        // In production, these would be actual links
        alert(`${platform} profile will open here`);
    });
});

// Parallax effect for mission icon
window.addEventListener('scroll', () => {
    const missionIcon = document.querySelector('.mission-icon');
    if (missionIcon) {
        const scrolled = window.pageYOffset;
        const rect = missionIcon.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
            missionIcon.style.transform = `translateY(${scrolled * 0.1}px) rotate(${scrolled * 0.05}deg)`;
        }
    }
});

// Animate opensource stats on scroll
const osStats = document.querySelectorAll('.os-stat');
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const number = entry.target.querySelector('.os-number');
            animateNumber(number);
        }
    });
}, { threshold: 0.5 });

osStats.forEach(stat => {
    statsObserver.observe(stat);
});

function animateNumber(element) {
    const text = element.textContent;
    const isNumeric = !isNaN(parseInt(text));
    
    if (isNumeric) {
        const target = parseInt(text);
        let current = 0;
        const increment = target / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target + '+';
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 30);
    }
}

// Easter egg: Konami code
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.key);
    konamiCode = konamiCode.slice(-10);
    
    if (konamiCode.join(',') === konamiSequence.join(',')) {
        activateEasterEgg();
    }
});

function activateEasterEgg() {
    const techLogos = document.querySelectorAll('.tech-logo');
    techLogos.forEach((logo, index) => {
        setTimeout(() => {
            logo.style.animation = 'spin 1s ease-in-out';
        }, index * 50);
    });
    
    console.log('🎉 Easter egg activated! You found the secret!');
}

// Add spin animation
const spinStyle = document.createElement('style');
spinStyle.textContent = `
    @keyframes spin {
        from { transform: rotate(0deg) scale(1); }
        50% { transform: rotate(180deg) scale(1.2); }
        to { transform: rotate(360deg) scale(1); }
    }
`;
document.head.appendChild(spinStyle);
