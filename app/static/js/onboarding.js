/**
 * JavaScript for handling the onboarding questionnaire flow
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize form elements
    initializeSliders();
    initializeLikertScales();
    setupFormValidation();
    handleCheckboxGroups();
});

/**
 * Initialize all slider inputs with their default values
 */
function initializeSliders() {
    document.querySelectorAll('input[type=range]').forEach(function(slider) {
        // Get the associated value display element
        const valueDisplayId = slider.id.replace('slider', 'value');
        const valueDisplay = document.getElementById(valueDisplayId);
        
        if (valueDisplay) {
            // Set initial value
            valueDisplay.innerText = slider.value;
            
            // Update value on input change
            slider.addEventListener('input', function() {
                valueDisplay.innerText = this.value;
            });
        }
    });
}

/**
 * Set up Likert scale inputs for better UX
 */
function initializeLikertScales() {
    // Add visual feedback when selecting a likert option
    document.querySelectorAll('.likert-option input').forEach(function(radio) {
        radio.addEventListener('change', function() {
            // Remove highlight class from all options in the same group
            const name = this.getAttribute('name');
            document.querySelectorAll(`input[name="${name}"]`).forEach(function(groupRadio) {
                groupRadio.closest('.likert-option').classList.remove('bg-light');
            });
            
            // Add highlight to the selected option
            this.closest('.likert-option').classList.add('bg-light');
        });
    });
}

/**
 * Set up form validation 
 */
function setupFormValidation() {
    const form = document.getElementById('questionnaireForm');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            // Check if all required questions are answered
            const unansweredRequiredQuestions = [];
            
            document.querySelectorAll('.question-container').forEach(function(container) {
                const inputs = container.querySelectorAll('input, select, textarea');
                const questionId = inputs.length > 0 ? inputs[0].name.replace('question_', '') : null;
                
                // Skip if no inputs or not required
                if (!questionId || !isQuestionRequired(container)) return;
                
                // Check if any input in this question group is filled
                const isAnswered = Array.from(inputs).some(input => {
                    if (input.type === 'radio' || input.type === 'checkbox') {
                        return input.checked;
                    } else {
                        return input.value.trim() !== '';
                    }
                });
                
                if (!isAnswered) {
                    unansweredRequiredQuestions.push(questionId);
                    highlightUnansweredQuestion(container);
                }
            });
            
            // If there are unanswered required questions, prevent form submission
            if (unansweredRequiredQuestions.length > 0) {
                event.preventDefault();
                alert('Please answer all required questions before continuing.');
                
                // Scroll to the first unanswered question
                const firstUnansweredQuestion = document.querySelector(`[name="question_${unansweredRequiredQuestions[0]}"]`);
                if (firstUnansweredQuestion) {
                    firstUnansweredQuestion.closest('.question-container').scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    }
}

/**
 * Check if a question is required
 */
function isQuestionRequired(questionContainer) {
    // This is a simplified check - in a real app you might check data attributes or other markers
    const inputs = questionContainer.querySelectorAll('input, select, textarea');
    return Array.from(inputs).some(input => input.required);
}

/**
 * Highlight an unanswered question
 */
function highlightUnansweredQuestion(container) {
    container.classList.add('border-danger');
    
    // Remove the highlight after a while
    setTimeout(() => {
        container.classList.remove('border-danger');
    }, 5000);
}

/**
 * Handle checkbox groups to collect multiple selections
 */
function handleCheckboxGroups() {
    const form = document.getElementById('questionnaireForm');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            // Process checkbox groups
            const checkboxGroups = {};
            
            // Find all checkboxes and group them by name
            document.querySelectorAll('input[type=checkbox]').forEach(function(checkbox) {
                const name = checkbox.getAttribute('name');
                
                if (!checkboxGroups[name]) {
                    checkboxGroups[name] = [];
                }
                
                if (checkbox.checked) {
                    checkboxGroups[name].push(checkbox.value);
                }
            });
            
            // For each group, create a hidden input with comma-separated values
            for (const [name, values] of Object.entries(checkboxGroups)) {
                // If group has at least one checked value
                if (values.length > 0) {
                    // Uncheck all boxes to avoid multiple submissions
                    document.querySelectorAll(`input[type=checkbox][name="${name}"]`).forEach(cb => {
                        cb.disabled = true; // Disable instead of unchecking to keep visual state
                    });
                    
                    // Create a hidden input with comma-separated values
                    const hiddenInput = document.createElement('input');
                    hiddenInput.type = 'hidden';
                    hiddenInput.name = name;
                    hiddenInput.value = values.join(',');
                    form.appendChild(hiddenInput);
                }
                // If no checkboxes were selected, add a "none" value
                else {
                    const hiddenInput = document.createElement('input');
                    hiddenInput.type = 'hidden';
                    hiddenInput.name = name;
                    hiddenInput.value = 'none';
                    form.appendChild(hiddenInput);
                }
            }
        });
    }
}