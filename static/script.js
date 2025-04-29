// Gallery Modal Functionality
function openModal(imageSrc) {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    
    modal.style.display = 'flex';
    modalImg.src = imageSrc;
    
    // Prevent scrolling when modal is open
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const modal = document.getElementById('imageModal');
    modal.style.display = 'none';
    
    // Re-enable scrolling
    document.body.style.overflow = 'auto';
}

// Close modal when clicking outside the image
window.onclick = function(event) {
    const modal = document.getElementById('imageModal');
    if (event.target === modal) {
        closeModal();
    }
}

// Form submission
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            
            // Change icon based on menu state
            const icon = this.querySelector('i');
            if (navLinks.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }
    
    // Close mobile menu when clicking on a link
    const links = document.querySelectorAll('.nav-link');
    links.forEach(link => {
        link.addEventListener('click', function() {
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                const icon = mobileMenuBtn.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    });
    
    // Language Switcher
    const langButtons = document.querySelectorAll('.lang-btn');
    langButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active class from all buttons
            langButtons.forEach(b => b.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Get language code
            const lang = this.getAttribute('data-lang');
            
            // Here you would typically implement language switching logic
            // For demonstration, we'll just log it
            console.log(`Switching to language: ${lang}`);
            
            // In a real implementation, you would load translations
            // and update the page content
            if (lang === 'en') {
                // Example of how you might update content
                document.querySelector('.hero h1').textContent = 'GlamStyle Barbershop';
                document.querySelector('.hero p').textContent = 'Experts in the art of cutting and male grooming';
                // ... update other elements
            } else if (lang === 'es') {
                document.querySelector('.hero h1').textContent = 'Peluquería GlamStyle';
                document.querySelector('.hero p').textContent = 'Expertos en el arte del corte y cuidado masculino';
                // ... update other elements
            }
        });
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // Account for fixed header
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    const contactForm = document.querySelector('.contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const subject = document.getElementById('subject').value;
            const message = document.getElementById('message').value;
            
            // Here you would typically send the data to a server
            // For demonstration, we'll just log it and show an alert
            console.log({
                name,
                email,
                subject,
                message
            });
            
            alert('¡Mensaje enviado con éxito! Te contactaremos pronto.');
            contactForm.reset();
        });
    }
});