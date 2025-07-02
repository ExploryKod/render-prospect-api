// Main JavaScript file for Prospects Flow Service

document.addEventListener('DOMContentLoaded', function() {
    console.log('Prospects Flow Service loaded successfully');
    
    // Add smooth scrolling to all links
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
    
    // Add loading animation to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('disabled')) {
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Chargement...';
                this.classList.add('disabled');
                
                // Reset button after 2 seconds (for demo purposes)
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('disabled');
                }, 2000);
            }
        });
    });
    
    // Add tooltip functionality
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Add card hover effects
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Add navbar scroll effect
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });
    
    // Add service status check
    checkServiceStatus();
});

// Function to check service status
async function checkServiceStatus() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        
        const statusElement = document.querySelector('.text-success');
        if (statusElement && data.status === 'healthy') {
            statusElement.innerHTML = '<i class="fas fa-check-circle me-2"></i>Service opérationnel';
            statusElement.className = 'text-success';
        } else {
            statusElement.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i>Service indisponible';
            statusElement.className = 'text-danger';
        }
    } catch (error) {
        console.error('Error checking service status:', error);
        const statusElement = document.querySelector('.text-success');
        if (statusElement) {
            statusElement.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i>Erreur de connexion';
            statusElement.className = 'text-warning';
        }
    }
}

// Function to show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Export functions for use in other scripts
window.ProspectsFlowService = {
    showNotification,
    checkServiceStatus
}; 