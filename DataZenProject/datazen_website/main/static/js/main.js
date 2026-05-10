// =====================================================
// DataZen Analytics - Interactive JavaScript
// Modern interactivity with animations and validations
// =====================================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive features
    initMobileMenu();
    initProfileDropdown();
    initSmoothScroll();
    initScrollAnimations();
    initFormValidation();
    initServiceCards();
    initCounterAnimation();
    initNewsletterForm();
    initPackagePricing();
    init3DNavbar();
    // REMOVED: initAjaxNavigation() - Disabled to fix page navigation issues
});

// DISABLED: AJAX navigation - Handle browser back/forward buttons
// window.addEventListener('popstate', function(event) {
//     if (event.state && event.state.content) {
//         loadPageContent(event.state.content, false);
//     }
// });

// =====================================================
// Mobile Menu Toggle
// =====================================================
function initMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    if (!hamburger) return;
    
    hamburger.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
    
    // Close menu when a link is clicked
    const navItems = document.querySelectorAll('.nav-links a');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            navLinks.classList.remove('active');
            hamburger.classList.remove('active');
        });
    });
}

// =====================================================
// Profile Dropdown Menu
// =====================================================
function initProfileDropdown() {
    const profileDropdown = document.querySelector('.user-profile-dropdown');
    
    if (!profileDropdown) return;
    
    // Toggle dropdown on click
    profileDropdown.addEventListener('click', function(e) {
        e.stopPropagation();
        this.classList.toggle('active');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.user-profile-dropdown')) {
            profileDropdown.classList.remove('active');
        }
    });
    
    // Close dropdown when menu item is clicked
    const profileMenuItems = document.querySelectorAll('.profile-menu-item');
    profileMenuItems.forEach(item => {
        item.addEventListener('click', function() {
            profileDropdown.classList.remove('active');
        });
    });
}

// =====================================================
// Smooth Scrolling for Internal Links
// =====================================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

// =====================================================
// Scroll Animations - Reveal elements on scroll
// =====================================================
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe cards, sections, and elements with animate-on-scroll class
    document.querySelectorAll('.card, .service-item, .package-card, .value-item, .stat-item, .project-card').forEach(el => {
        el.classList.add('observe-element');
        observer.observe(el);
    });
}

// =====================================================
// Form Validation
// =====================================================
function initFormValidation() {
    const contactForm = document.querySelector('.contact-form');
    if (!contactForm) return;
    
    contactForm.addEventListener('submit', function(e) {
        const formData = new FormData(this);
        const name = formData.get('name').trim();
        const email = formData.get('email').trim();
        const message = formData.get('message').trim();
        
        // Validation
        let isValid = true;
        let errors = [];
        
        if (!name || name.length < 2) {
            errors.push('Please enter a valid name (at least 2 characters)');
            isValid = false;
        }
        
        if (!email || !isValidEmail(email)) {
            errors.push('Please enter a valid email address');
            isValid = false;
        }
        
        if (!message || message.length < 10) {
            errors.push('Message must be at least 10 characters long');
            isValid = false;
        }
        
        // Show validation feedback
        const feedbackDiv = document.querySelector('.form-feedback') || createFeedbackDiv(contactForm);
        
        if (!isValid) {
            e.preventDefault();
            feedbackDiv.className = 'form-feedback error';
            feedbackDiv.innerHTML = '✗ Please fix the following:<br>' + errors.join('<br>');
            feedbackDiv.style.display = 'block';
        } else {
            feedbackDiv.className = 'form-feedback success';
            feedbackDiv.textContent = '✓ Validating your message...';
            feedbackDiv.style.display = 'block';
        }
    });
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function createFeedbackDiv(form) {
    const feedback = document.createElement('div');
    feedback.className = 'form-feedback';
    form.parentNode.insertBefore(feedback, form);
    return feedback;
}

// =====================================================
// Interactive Service Cards - Expand/Collapse
// =====================================================
function initServiceCards() {
    const serviceItems = document.querySelectorAll('.service-item');
    
    serviceItems.forEach(item => {
        const header = item.querySelector('.service-header');
        if (header) {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                item.classList.toggle('expanded');
            });
        }
    });
}

// =====================================================
// Counter Animation - Animate statistics numbers
// =====================================================
function initCounterAnimation() {
    const statItems = document.querySelectorAll('.stat-item h3');
    const animatedElements = new Set();
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting && !animatedElements.has(entry.target)) {
                animateCounter(entry.target);
                animatedElements.add(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    statItems.forEach(item => observer.observe(item));
}

function animateCounter(element) {
    const finalValue = element.textContent;
    const numberMatch = finalValue.match(/\d+/);
    
    if (!numberMatch) return;
    
    const endValue = parseInt(numberMatch[0]);
    const suffix = finalValue.replace(/\d+/, '').trim();
    let currentValue = 0;
    const increment = endValue / 30; // 30 steps for smooth animation
    const duration = 1000; // 1 second
    const startTime = Date.now();
    
    function update() {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        currentValue = Math.floor(endValue * progress);
        element.textContent = currentValue + suffix;
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    update();
}

// =====================================================
// Newsletter Form
// =====================================================
function initNewsletterForm() {
    const newsletterForm = document.querySelector('.newsletter-form');
    if (!newsletterForm) return;
    
    newsletterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const input = this.querySelector('input[type="email"]');
        const button = this.querySelector('button');
        const email = input.value.trim();
        
        if (!email || !isValidEmail(email)) {
            showNotification('Please enter a valid email address', 'error');
            return;
        }
        
        const originalText = button.textContent;
        button.textContent = 'Subscribing...';
        button.disabled = true;
        
        // Simulate subscription
        setTimeout(() => {
            button.textContent = 'Subscribed! ✓';
            input.value = '';
            showNotification('Successfully subscribed to our newsletter!', 'success');
            
            setTimeout(() => {
                button.textContent = originalText;
                button.disabled = false;
            }, 2000);
        }, 800);
    });
}

// =====================================================
// Package Pricing Interactive
// =====================================================
function initPackagePricing() {
    const packageCards = document.querySelectorAll('.package-card');
    
    packageCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.zIndex = '10';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.zIndex = 'auto';
        });
        
        const button = card.querySelector('.btn');
        if (button) {
            button.addEventListener('click', handlePackageClick);
        }
    });
}

function handlePackageClick(e) {
    const packageName = e.target.closest('.package-card').querySelector('h3').textContent;
    const message = `I'm interested in the ${packageName} plan.`;
    const contactLink = document.querySelector('a[href*="contact"]');
    
    if (contactLink) {
        // Store the message and navigate to contact page
        sessionStorage.setItem('selectedPackage', message);
        window.location.href = contactLink.href;
    }
}

// =====================================================
// Notification System
// =====================================================
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#4caf50' : '#f44336'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 9999;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// =====================================================
// Scroll to Top Button
// =====================================================
function initScrollToTop() {
    const scrollButton = document.querySelector('.scroll-to-top');
    if (!scrollButton) {
        createScrollToTopButton();
    }
    
    window.addEventListener('scroll', function() {
        const button = document.querySelector('.scroll-to-top');
        if (window.pageYOffset > 300) {
            button.style.display = 'block';
        } else {
            button.style.display = 'none';
        }
    });
}

function createScrollToTopButton() {
    const button = document.createElement('button');
    button.className = 'scroll-to-top';
    button.innerHTML = '↑';
    button.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        padding: 12px 16px;
        background: #1a73e8;
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        display: none;
        z-index: 999;
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.3);
        transition: all 0.3s ease;
        font-size: 1.5rem;
        line-height: 1;
    `;
    
    button.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    
    button.addEventListener('mouseenter', function() {
        this.style.background = '#00bcd4';
        this.style.transform = 'scale(1.1)';
    });
    
    button.addEventListener('mouseleave', function() {
        this.style.background = '#1a73e8';
        this.style.transform = 'scale(1)';
    });
    
    document.body.appendChild(button);
}

initScrollToTop();

// =====================================================
// Keyboard Navigation
// =====================================================
document.addEventListener('keydown', function(e) {
    // Close mobile menu on Escape
    if (e.key === 'Escape') {
        const navLinks = document.querySelector('.nav-links');
        const hamburger = document.querySelector('.hamburger');
        if (navLinks && hamburger) {
            navLinks.classList.remove('active');
            hamburger.classList.remove('active');
        }
    }
});

// =====================================================
// 3D Navbar Scroll Effect
// =====================================================
function init3DNavbar() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// =====================================================
// Add Loading Animation for Links
// =====================================================
document.querySelectorAll('a:not([href*="javascript"])').forEach(link => {
    link.addEventListener('click', function(e) {
        if (this.hasAttribute('download') || this.target === '_blank' || this.href.includes('#')) {
            return;
        }
        
        // Add loading state for external navigation
        const clickedLink = this;
        setTimeout(() => {
            document.body.style.opacity = '0.7';
        }, 100);
    });
});

// =====================================================
// Enhanced Social Media Links with App Opening
// =====================================================
function initEnhancedSocialLinks() {
    const socialLinks = document.querySelectorAll('.social-link');
    
    socialLinks.forEach(link => {
        // Add ripple effect on click
        link.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            ripple.style.left = e.clientX - this.getBoundingClientRect().left + 'px';
            ripple.style.top = e.clientY - this.getBoundingClientRect().top + 'px';
            this.appendChild(ripple);
            
            // Remove ripple after animation
            setTimeout(() => ripple.remove(), 600);
            
            // Add glow animation
            this.style.animation = 'pulse 0.6s ease';
            setTimeout(() => {
                this.style.animation = 'none';
            }, 600);
        });
        
        // Add entrance animation
        link.style.animation = `slideInUp 0.6s ease backwards`;
        link.style.animationDelay = `${socialLinks.length - Array.from(socialLinks).indexOf(link) * 0.1}s`;
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initEnhancedSocialLinks);

// Add CSS for ripple effect dynamically
const style = document.createElement('style');
style.textContent = `
    .social-link {
        position: relative;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        pointer-events: none;
        animation: ripple-animation 0.6s ease-out;
        transform: translate(-50%, -50%);
    }
    
    @keyframes ripple-animation {
        0% {
            width: 0;
            height: 0;
            opacity: 1;
        }
        100% {
            width: 300px;
            height: 300px;
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// =====================================================
// =====================================================
// AJAX Navigation - DISABLED to fix page navigation issues
// =====================================================
// All navigation now uses standard full-page loads
/*
function initAjaxNavigation() {
    // DISABLED - was causing refresh issues
}

function loadPageAjax(url) {
    // DISABLED - was causing refresh issues  
}
*/

function loadPageContent(content, updateHistory = true) {
    const mainContent = document.querySelector('.main-content');
    
    if (mainContent) {
        mainContent.style.transition = 'opacity 0.3s ease';
        mainContent.style.opacity = '0';
        
        setTimeout(() => {
            mainContent.innerHTML = content;
            mainContent.style.opacity = '1';
            
            // Re-initialize page scripts
            reinitializePageScripts();
            
            // Scroll to top
            window.scrollTo({top: 0, behavior: 'smooth'});
        }, 300);
    }
}

function reinitializePageScripts() {
    // Re-run all initialization functions for new content
    initSmoothScroll();
    initScrollAnimations();
    initFormValidation();
    initServiceCards();
    initCounterAnimation();
    initNewsletterForm();
    initPackagePricing();
}
