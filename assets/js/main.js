// Premium Car Rental - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips and other interactive elements
    initializeTooltips();
    initializeFormValidation();
    initializeImagePreview();
    initializeDatePickers();
    initializeSearchFilters();
});

// Initialize tooltips
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            tooltip.style.position = 'absolute';
            tooltip.style.background = '#333';
            tooltip.style.color = '#fff';
            tooltip.style.padding = '5px 10px';
            tooltip.style.borderRadius = '4px';
            tooltip.style.fontSize = '12px';
            tooltip.style.zIndex = '1000';
            tooltip.style.whiteSpace = 'nowrap';
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
            
            this.tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this.tooltip) {
                this.tooltip.remove();
                this.tooltip = null;
            }
        });
    });
}

// Initialize form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });
}

// Validate form
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'This field is required');
            isValid = false;
        } else {
            clearFieldError(field);
            
            // Email validation
            if (field.type === 'email') {
                if (!validateEmail(field.value)) {
                    showFieldError(field, 'Please enter a valid email address');
                    isValid = false;
                }
            }
            
            // Phone validation
            if (field.name === 'phone') {
                if (!validatePhone(field.value)) {
                    showFieldError(field, 'Please enter a valid 10-digit phone number');
                    isValid = false;
                }
            }
            
            // Password validation
            if (field.name === 'password') {
                if (field.value.length < 6) {
                    showFieldError(field, 'Password must be at least 6 characters long');
                    isValid = false;
                }
            }
            
            // Confirm password validation
            if (field.name === 'confirm_password') {
                const passwordField = form.querySelector('[name="password"]');
                if (passwordField && field.value !== passwordField.value) {
                    showFieldError(field, 'Passwords do not match');
                    isValid = false;
                }
            }
        }
    });
    
    return isValid;
}

// Show field error
function showFieldError(field, message) {
    clearFieldError(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.color = '#e74c3c';
    errorDiv.style.fontSize = '12px';
    errorDiv.style.marginTop = '5px';
    
    field.style.borderColor = '#e74c3c';
    field.parentNode.appendChild(errorDiv);
    field.errorElement = errorDiv;
}

// Clear field error
function clearFieldError(field) {
    if (field.errorElement) {
        field.errorElement.remove();
        field.errorElement = null;
    }
    field.style.borderColor = '';
}

// Validate email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate phone
function validatePhone(phone) {
    const re = /^[0-9]{10}$/;
    return re.test(phone);
}

// Initialize image preview
function initializeImagePreview() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let preview = input.parentNode.querySelector('.image-preview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.className = 'image-preview';
                        preview.style.maxWidth = '200px';
                        preview.style.maxHeight = '150px';
                        preview.style.marginTop = '10px';
                        preview.style.borderRadius = '8px';
                        preview.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
                        input.parentNode.appendChild(preview);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });
}

// Initialize date pickers
function initializeDatePickers() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    
    dateInputs.forEach(input => {
        // Set minimum date to today
        if (input.hasAttribute('data-min-today')) {
            input.min = today;
        }
        
        // Add date change event
        input.addEventListener('change', function() {
            if (this.value < today) {
                this.value = today;
                showFieldError(this, 'Date cannot be in the past');
            } else {
                clearFieldError(this);
            }
        });
    });
}

// Initialize search filters
function initializeSearchFilters() {
    const searchForm = document.querySelector('#search-form');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="search"]');
        const seatingSelect = searchForm.querySelector('select[name="seating_capacity"]');
        
        // Auto-submit on change
        if (seatingSelect) {
            seatingSelect.addEventListener('change', function() {
                searchForm.submit();
            });
        }
        
        // Search on enter with debounce
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    searchForm.submit();
                }, 500);
            });
        }
    }
}

// Show alert message
function showAlert(message, type = 'success') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    alert.style.position = 'fixed';
    alert.style.top = '20px';
    alert.style.right = '20px';
    alert.style.zIndex = '9999';
    alert.style.maxWidth = '300px';
    alert.style.padding = '15px';
    alert.style.borderRadius = '8px';
    alert.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
    
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.style.opacity = '0';
        alert.style.transition = 'opacity 0.3s ease';
        setTimeout(() => alert.remove(), 300);
    }, 3000);
}

// Confirm action
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Calculate rental cost
function calculateRentalCost(rentPerDay, numberOfDays) {
    return rentPerDay * numberOfDays;
}

// AJAX helper function
function ajaxRequest(url, method, data, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            callback(JSON.parse(xhr.responseText));
        }
    };
    
    const params = typeof data === 'string' ? data : Object.keys(data).map(key => 
        encodeURIComponent(key) + '=' + encodeURIComponent(data[key])
    ).join('&');
    
    xhr.send(params);
}

// Loading spinner
function showLoading(element) {
    const spinner = document.createElement('div');
    spinner.className = 'loading-spinner';
    spinner.innerHTML = '⏳ Loading...';
    spinner.style.textAlign = 'center';
    spinner.style.padding = '20px';
    spinner.style.fontSize = '16px';
    spinner.style.color = '#666';
    
    element.appendChild(spinner);
    return spinner;
}

function hideLoading(spinner) {
    if (spinner) {
        spinner.remove();
    }
}

// Smooth scroll
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Print function
function printPage() {
    window.print();
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Copied to clipboard!', 'success');
    }).catch(() => {
        showAlert('Failed to copy to clipboard', 'error');
    });
}
