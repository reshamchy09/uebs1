// static/js/main.js

// ===== GLOBAL VARIABLES =====
let scene, camera, renderer, particles, animationId;
const mouse = { x: 0, y: 0 };

// ===== DOM CONTENT LOADED =====
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// ===== INITIALIZE APPLICATION =====
function initializeApp() {
    // Initialize components
    initLoader();
    initNavigation();
    initThreeJS();
    initAOS();
    initCounters();
    initScrollAnimations();
    initFormAnimations();
    initTickerAnimation();
    
    // Initialize GSAP animations
    initGSAPAnimations();
    
    // Handle window resize
    window.addEventListener('resize', onWindowResize);
}

// ===== LOADER =====
function initLoader() {
    const loader = document.getElementById('loader');
    
    // Hide loader after 2 seconds
    setTimeout(() => {
        if (loader) {
            loader.style.opacity = '0';
            setTimeout(() => {
                loader.style.display = 'none';
            }, 500);
        }
    }, 1000);
}

// ===== NAVIGATION =====
function initNavigation() {
    const navbar = document.getElementById('navbar');
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    
    // Scroll effect for navbar
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Mobile menu toggle
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
        
        // Close menu when clicking on nav links
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
            });
        });
    }
    
    // Smooth scroll for navigation links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ===== THREE.JS SCENE =====
function initThreeJS() {
    const sceneContainer = document.getElementById('three-scene');
    if (!sceneContainer) return;
    
    // Scene setup
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0x000000, 0);
    sceneContainer.appendChild(renderer.domElement);
    
    // Create floating geometric shapes
    createFloatingShapes();
    
    // Create particle system
    createParticleSystem();
    
    // Position camera
    camera.position.z = 5;
    
    // Mouse interaction
    document.addEventListener('mousemove', onMouseMove);
    
    // Start animation loop
    animate();
}

function createFloatingShapes() {
    const geometries = [
        new THREE.BoxGeometry(0.5, 0.5, 0.5),
        new THREE.SphereGeometry(0.3, 16, 16),
        new THREE.ConeGeometry(0.3, 0.8, 8),
        new THREE.OctahedronGeometry(0.4)
    ];
    
    const materials = [
        new THREE.MeshBasicMaterial({ color: 0xFFD700, wireframe: true }),
        new THREE.MeshBasicMaterial({ color: 0x004080, wireframe: true }),
        new THREE.MeshBasicMaterial({ color: 0xFFFFFF, wireframe: true })
    ];
    
    for (let i = 0; i < 15; i++) {
        const geometry = geometries[Math.floor(Math.random() * geometries.length)];
        const material = materials[Math.floor(Math.random() * materials.length)];
        const mesh = new THREE.Mesh(geometry, material);
        
        mesh.position.x = (Math.random() - 0.5) * 20;
        mesh.position.y = (Math.random() - 0.5) * 20;
        mesh.position.z = (Math.random() - 0.5) * 20;
        
        mesh.rotation.x = Math.random() * Math.PI;
        mesh.rotation.y = Math.random() * Math.PI;
        
        mesh.userData = {
            rotationSpeed: {
                x: (Math.random() - 0.5) * 0.02,
                y: (Math.random() - 0.5) * 0.02,
                z: (Math.random() - 0.5) * 0.02
            },
            floatSpeed: Math.random() * 0.02 + 0.01
        };
        
        scene.add(mesh);
    }
}

function createParticleSystem() {
    const particleCount = 1000;
    const positions = new Float32Array(particleCount * 3);
    const velocities = new Float32Array(particleCount * 3);
    
    for (let i = 0; i < particleCount; i++) {
        positions[i * 3] = (Math.random() - 0.5) * 50;
        positions[i * 3 + 1] = (Math.random() - 0.5) * 50;
        positions[i * 3 + 2] = (Math.random() - 0.5) * 50;
        
        velocities[i * 3] = (Math.random() - 0.5) * 0.02;
        velocities[i * 3 + 1] = (Math.random() - 0.5) * 0.02;
        velocities[i * 3 + 2] = (Math.random() - 0.5) * 0.02;
    }
    
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    
    const material = new THREE.PointsMaterial({
        color: 0xFFD700,
        size: 2,
        transparent: true,
        opacity: 0.6
    });
    
    particles = new THREE.Points(geometry, material);
    particles.userData = { velocities: velocities };
    scene.add(particles);
}

function animate() {
    animationId = requestAnimationFrame(animate);
    
    // Animate floating shapes
    scene.children.forEach(child => {
        if (child.userData && child.userData.rotationSpeed) {
            child.rotation.x += child.userData.rotationSpeed.x;
            child.rotation.y += child.userData.rotationSpeed.y;
            child.rotation.z += child.userData.rotationSpeed.z;
            
            // Floating animation
            child.position.y += Math.sin(Date.now() * child.userData.floatSpeed) * 0.001;
        }
    });
    
    // Animate particles
    if (particles) {
        const positions = particles.geometry.attributes.position.array;
        const velocities = particles.userData.velocities;
        
        for (let i = 0; i < positions.length; i += 3) {
            positions[i] += velocities[i];
            positions[i + 1] += velocities[i + 1];
            positions[i + 2] += velocities[i + 2];
            
            // Wrap around boundaries
            if (positions[i] > 25) positions[i] = -25;
            if (positions[i] < -25) positions[i] = 25;
            if (positions[i + 1] > 25) positions[i + 1] = -25;
            if (positions[i + 1] < -25) positions[i + 1] = 25;
            if (positions[i + 2] > 25) positions[i + 2] = -25;
            if (positions[i + 2] < -25) positions[i + 2] = 25;
        }
        
        particles.geometry.attributes.position.needsUpdate = true;
    }
    
    // Camera movement based on mouse
    camera.position.x += (mouse.x * 2 - camera.position.x) * 0.02;
    camera.position.y += (-mouse.y * 2 - camera.position.y) * 0.02;
    camera.lookAt(scene.position);
    
    renderer.render(scene, camera);
}

function onMouseMove(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
}

function onWindowResize() {
    if (camera && renderer) {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }
}

// ===== AOS INITIALIZATION =====
function initAOS() {
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 1000,
            easing: 'ease-in-out',
            once: true,
            offset: 100
        });
    }
}

// ===== COUNTER ANIMATION =====
function initCounters() {
    const counters = document.querySelectorAll('.stat-number[data-count]');
    
    const countUp = (element) => {
        const target = parseInt(element.getAttribute('data-count'));
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += step;
            element.textContent = Math.floor(current);
            
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            }
        }, 16);
    };
    
    // Intersection Observer for counters
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                countUp(entry.target);
                observer.unobserve(entry.target);
            }
        });
    });
    
    counters.forEach(counter => observer.observe(counter));
}

// ===== GSAP ANIMATIONS =====
function initGSAPAnimations() {
    if (typeof gsap === 'undefined') return;
    
    // Hero text animation
    gsap.timeline({ delay: 2.5 })
        .from('.hero-title', { duration: 1, y: 100, opacity: 0, ease: 'power3.out' })
        .from('.hero-subtitle', { duration: 0.8, y: 50, opacity: 0, ease: 'power3.out' }, '-=0.5')
        .from('.hero-buttons .btn', { duration: 0.6, y: 30, opacity: 0, stagger: 0.2, ease: 'power3.out' }, '-=0.3');
    
    // Floating elements animation
    gsap.to('.floating-book', { duration: 6, y: -30, rotation: 15, ease: 'power2.inOut', repeat: -1, yoyo: true });
    gsap.to('.floating-globe', { duration: 8, y: -40, rotation: -10, ease: 'power2.inOut', repeat: -1, yoyo: true, delay: 1 });
    gsap.to('.floating-trophy', { duration: 7, y: -35, rotation: 8, ease: 'power2.inOut', repeat: -1, yoyo: true, delay: 2 });
    
    // Page scroll animations
    gsap.registerPlugin(ScrollTrigger);
    
    // Feature cards animation
    gsap.from('.feature-card', {
        scrollTrigger: '.features-section',
        duration: 0.8,
        y: 100,
        opacity: 0,
        stagger: 0.2,
        ease: 'power3.out'
    });
    
    // Stats animation
    gsap.from('.stat-card', {
        scrollTrigger: '.stats-section',
        duration: 1,
        scale: 0.8,
        opacity: 0,
        stagger: 0.15,
        ease: 'back.out(1.7)'
    });
}

// ===== SCROLL ANIMATIONS =====
function initScrollAnimations() {
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('[data-scroll-animate]');
        
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight * 0.8) {
                element.classList.add('animated');
            }
        });
    };
    
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Initial check
}

// ===== FORM ANIMATIONS =====
function initFormAnimations() {
    const formFields = document.querySelectorAll('input, textarea, select');
    
    formFields.forEach(field => {
        // Floating labels
        field.addEventListener('focus', () => {
            field.parentElement.classList.add('focused');
        });
        
        field.addEventListener('blur', () => {
            if (!field.value) {
                field.parentElement.classList.remove('focused');
            }
        });
        
        // Check if field has value on load
        if (field.value) {
            field.parentElement.classList.add('focused');
        }
    });
    
    // Form validation and submission
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
                submitBtn.disabled = true;
            }
        });
    });
}

// ===== TICKER ANIMATION =====
function initTickerAnimation() {
    const ticker = document.querySelector('.ticker-content');
    if (!ticker) return;
    
    // Clone ticker content for seamless loop
    const tickerText = ticker.innerHTML;
    ticker.innerHTML = tickerText + tickerText;
}

// ===== IMAGE LAZY LOADING =====
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// ===== 3D CAROUSEL =====
function init3DCarousel() {
    const carousel = document.querySelector('.carousel-3d');
    if (!carousel) return;
    
    const items = carousel.querySelectorAll('.carousel-item');
    const totalItems = items.length;
    let currentItem = 0;
    
    const updateCarousel = () => {
        items.forEach((item, index) => {
            const angle = (360 / totalItems) * (index - currentItem);
            const translateZ = 300;
            
            item.style.transform = `rotateY(${angle}deg) translateZ(${translateZ}px)`;
            item.style.opacity = index === currentItem ? 1 : 0.7;
        });
    };
    
    // Auto-rotate carousel
    setInterval(() => {
        currentItem = (currentItem + 1) % totalItems;
        updateCarousel();
    }, 3000);
    
    updateCarousel();
}

// ===== PARALLAX SCROLLING =====
function initParallax() {
    const parallaxElements = document.querySelectorAll('.parallax-element');
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.speed || 0.5;
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });
}

// ===== MODAL FUNCTIONALITY =====
function initModals() {
    const modalTriggers = document.querySelectorAll('[data-modal]');
    const modals = document.querySelectorAll('.modal');
    const closeButtons = document.querySelectorAll('.modal-close');
    
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            const modalId = trigger.dataset.modal;
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        });
    });
    
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const modal = button.closest('.modal');
            if (modal) {
                modal.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        });
    });
    
    // Close modal on outside click
    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        });
    });
}

// ===== SEARCH FUNCTIONALITY =====
function initSearch() {
    const searchInput = document.querySelector('#search-input');
    const searchResults = document.querySelector('#search-results');
    
    if (!searchInput) return;
    
    let searchTimeout;
    
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        const query = e.target.value.trim();
        
        if (query.length < 2) {
            searchResults.innerHTML = '';
            return;
        }
        
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    });
}

function performSearch(query) {
    // This would typically make an AJAX call to the Django backend
    // For now, we'll simulate search results
    const mockResults = [
        { title: 'Academic Programs', url: '/academics/', type: 'page' },
        { title: 'Admission Requirements', url: '/admissions/', type: 'page' },
        { title: 'Faculty Members', url: '/faculty/', type: 'page' }
    ];
    
    const filteredResults = mockResults.filter(item => 
        item.title.toLowerCase().includes(query.toLowerCase())
    );
    
    displaySearchResults(filteredResults);
}

function displaySearchResults(results) {
    const searchResults = document.querySelector('#search-results');
    if (!searchResults) return;
    
    if (results.length === 0) {
        searchResults.innerHTML = '<div class="no-results">No results found</div>';
        return;
    }
    
    const resultsHTML = results.map(result => `
        <div class="search-result-item">
            <a href="${result.url}">
                <h4>${result.title}</h4>
                <span class="result-type">${result.type}</span>
            </a>
        </div>
    `).join('');
    
    searchResults.innerHTML = resultsHTML;
}

// ===== THEME SWITCHER =====
function initThemeSwitcher() {
    const themeToggle = document.querySelector('#theme-toggle');
    if (!themeToggle) return;
    
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
}

// ===== NOTIFICATION SYSTEM =====
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        hideNotification(notification);
    }, 5000);
    
    // Close button functionality
    notification.querySelector('.notification-close').addEventListener('click', () => {
        hideNotification(notification);
    });
}

function hideNotification(notification) {
    notification.classList.remove('show');
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 300);
}

// ===== UTILITY FUNCTIONS =====
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ===== CLEANUP ON PAGE UNLOAD =====
window.addEventListener('beforeunload', () => {
    if (animationId) {
        cancelAnimationFrame(animationId);
    }
    
    // Clean up Three.js resources
    if (scene) {
        scene.traverse((object) => {
            if (object.geometry) object.geometry.dispose();
            if (object.material) {
                if (Array.isArray(object.material)) {
                    object.material.forEach(material => material.dispose());
                } else {
                    object.material.dispose();
                }
            }
        });
    }
    
    if (renderer) {
        renderer.dispose();
    }
});

// ===== EXPORT FOR GLOBAL ACCESS =====
window.SchoolWebsite = {
    showNotification,
    hideNotification
};