/**
 * Codesphere – Website JavaScript
 * Moderni, minimaalinen funktionaalisuus
 */

document.addEventListener('DOMContentLoaded', function() {
    // === MOBILE MENU ===
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            mobileMenuBtn.classList.toggle('active');
        });
        
        // Sulje menu kun klikataan linkkiä
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
            });
        });
    }
    
    // === SMOOTH SCROLL ===
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // === HEADER SCROLL EFFECT ===
    const header = document.querySelector('.header');
    let lastScroll = 0;
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.boxShadow = 'none';
        }
        
        lastScroll = currentScroll;
    });
    
    // === FORM HANDLING ===
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Kerää lomakkeen tiedot
            const formData = new FormData(contactForm);
            const data = Object.fromEntries(formData);
            
            // Tässä lähetettäisiin data backendille
            // Nyt näytetään vain ilmoitus
            
            // Luo success-viesti
            const successMessage = document.createElement('div');
            successMessage.className = 'form-success';
            successMessage.innerHTML = `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 11.08V12a10 10 0 11-5.93-9.14"/>
                    <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
                <p><strong>Kiitos viestistäsi!</strong><br>Otamme sinuun yhteyttä pian.</p>
            `;
            successMessage.style.cssText = `
                display: flex;
                align-items: center;
                gap: 1rem;
                padding: 1.5rem;
                background-color: #d1fae5;
                border-radius: 8px;
                color: #065f46;
                margin-top: 1rem;
            `;
            successMessage.querySelector('svg').style.cssText = `
                width: 48px;
                height: 48px;
                flex-shrink: 0;
                color: #059669;
            `;
            
            // Piilota lomake ja näytä viesti
            contactForm.style.display = 'none';
            contactForm.parentNode.appendChild(successMessage);
            
            // Lokita konsoliin (kehitystä varten)
            console.log('Form submitted:', data);
        });
    }
    
    // === INTERSECTION OBSERVER FOR ANIMATIONS ===
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements
    document.querySelectorAll('.service-card, .team-card, .testimonial-card, .why-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
    
    // Add visible class styles
    const style = document.createElement('style');
    style.textContent = `
        .service-card.visible,
        .team-card.visible,
        .testimonial-card.visible,
        .why-card.visible {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
        
        .nav-links.active {
            display: flex;
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            flex-direction: column;
            padding: 1rem;
            background: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .nav-links.active a {
            padding: 0.75rem 1rem;
        }
        
        .mobile-menu-btn.active span:nth-child(1) {
            transform: rotate(45deg) translate(5px, 5px);
        }
        
        .mobile-menu-btn.active span:nth-child(2) {
            opacity: 0;
        }
        
        .mobile-menu-btn.active span:nth-child(3) {
            transform: rotate(-45deg) translate(5px, -5px);
        }
    `;
    document.head.appendChild(style);
    
    // === LAZY LOAD IMAGES (if any) ===
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window && lazyImages.length > 0) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    }
});

// === UTILITY FUNCTIONS ===

/**
 * Debounce function for scroll events
 */
function debounce(func, wait = 20, immediate = true) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

/**
 * Format phone number for display
 */
function formatPhoneNumber(phone) {
    return phone.replace(/(\+358)(\d{2})(\d{3})(\d{4})/, '$1 $2 $3 $4');
}
