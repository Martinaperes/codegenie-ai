/**
 * Main function to handle actions (generate, explain, debug) triggered by buttons.
 * @param {string} actionType - The type of action requested by the user.
 */
async function handleAction(actionType) {
    const inputElement = document.getElementById('user-input');
    const responseElement = document.getElementById('ai-response');
    const loadingElement = document.getElementById('loading');
    
    // Get the user's input text
    const prompt = inputElement.value.trim();

    // Basic Validation: Don't send empty requests to the server
    if (!prompt) {
        alert("Please enter some text or code first.");
        inputElement.focus();
        return;
    }

    // Prepare the UI for loading state
    responseElement.classList.add('hidden'); // Hide any previous response
    loadingElement.classList.remove('hidden'); // Show the loading spinner

    try {
        // Send an AJAX POST request to our Flask backend using fetch API
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // Serialize prompt and type into JSON format
            body: JSON.stringify({
                prompt: prompt,
                type: actionType
            })
        });

        // Parse the JSON response returned from the server
        const data = await response.json();

        // Hide spinner once we get a response
        loadingElement.classList.add('hidden');
        responseElement.classList.remove('hidden');

        // Check if the server returned an error (e.g., status 400 or 500)
        if (!response.ok) {
            responseElement.innerHTML = `<span class="error-text">❌ Error: ${data.error}</span>`;
            return;
        }

        // Display the successful AI response
        // Using textContent instead of innerHTML prevents XSS (Cross-Site Scripting) attacks
        // It correctly displays raw code without rendering it as HTML tags
        responseElement.textContent = data.response;

    } catch (error) {
        // Catch network errors (e.g., server offline, CORS issues)
        console.error("Fetch error:", error);
        loadingElement.classList.add('hidden');
        responseElement.classList.remove('hidden');
        responseElement.innerHTML = `<span class="error-text">❌ Network error. Make sure the Flask server is running.</span>`;
    }
}

/**
 * Function to copy the generated AI response to the user's clipboard.
 */
function copyToClipboard() {
    const responseElement = document.getElementById('ai-response');
    const textToCopy = responseElement.textContent;
    
    // Validate that there's actual generated text to copy
    // We don't want to copy the placeholder or error messages
    if (textToCopy && 
        !responseElement.querySelector('.placeholder-text') && 
        !responseElement.querySelector('.error-text')) {
            
        // Use modern Clipboard API
        navigator.clipboard.writeText(textToCopy).then(() => {
            // Provide visual feedback by changing the button text temporarily
            const copyBtn = document.getElementById('btn-copy');
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = "✅ Copied!";
            
            // Revert the button text after 2 seconds
            setTimeout(() => {
                copyBtn.innerHTML = originalText;
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy text: ', err);
            alert('Failed to copy text to clipboard.');
        });
    } else {
        alert("Nothing to copy yet! Please generate a response first.");
    }
}
