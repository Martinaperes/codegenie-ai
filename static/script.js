/**
 * CodeGenie AI - Core Frontend Controller
 * - Markdown Rendering (Marked.js Integration)
 * - Syntax Highlighting (Prism.js Integration)
 * - Modern Async Error Handling
 */

// Configure Marked options for better Markdown rendering
if (typeof marked !== 'undefined') {
    marked.setOptions({
        breaks: true,
        gfm: true,
        headerIds: false,
        mangle: false,
        highlight: function(code, lang) {
            // Optional: You can do extra pre-processing here if needed
            return code;
        }
    });
}

/**
 * Main function to handle actions (generate, explain, debug)
 * @param {string} actionType - The type of action requested
 */
async function handleAction(actionType) {
    const inputElement = document.getElementById('user-input');
    const responseElement = document.getElementById('ai-response');
    const loadingElement = document.getElementById('loading');
    
    // 1. Get and Validate Input
    const prompt = inputElement.value.trim();
    if (!prompt) {
        inputElement.animate([{ transform: 'translateX(-5px)' }, { transform: 'translateX(5px)' }], { duration: 100, iterations: 2 });
        inputElement.focus();
        return;
    }

    // 2. Prepare Loading State
    responseElement.innerHTML = ""; // Clear old output
    responseElement.classList.add('hidden');
    loadingElement.classList.remove('hidden');

    try {
        // 3. API Dispatch to Flask
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: prompt, type: actionType })
        });

        const data = await response.json();

        // 4. Teardown Loading State
        loadingElement.classList.add('hidden');
        responseElement.classList.remove('hidden');

        // 5. Handle Response
        if (!response.ok) {
            showError(`⚠️ Server Error: ${data.error || 'Unknown issue'}`);
            return;
        }

        // 6. Render as Markdown and Highlight
        renderResponse(data.response);

    } catch (error) {
        console.error("Fetch Exception:", error);
        loadingElement.classList.add('hidden');
        responseElement.classList.remove('hidden');
        showError("❌ CONNECTION FAILED: The CodeGenie uplink is offline. Please ensure your Python server is running.");
    }
}

/**
 * Renders the raw text response into formatted HTML via Markdown
 * @param {string} content - Raw AI text response
 */
function renderResponse(content) {
    const responseElement = document.getElementById('ai-response');
    
    // Parse Markdown to HTML
    if (typeof marked !== 'undefined') {
        const renderedHtml = marked.parse(content);
        responseElement.innerHTML = renderedHtml;
        
        // Wrap every <pre> block and add a copy button
        injectCodeCopyButtons();

        // Trigger Prism syntax highlighting
        if (typeof Prism !== 'undefined') {
            Prism.highlightAll();
        }
    } else {
        responseElement.textContent = content;
    }
}

/**
 * Finds all <pre> tags and adds a floating copy button
 */
function injectCodeCopyButtons() {
    const responseElement = document.getElementById('ai-response');
    const preBlocks = responseElement.querySelectorAll('pre');

    preBlocks.forEach((pre) => {
        // Create wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'pre-container';
        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(pre);

        // Create button
        const btn = document.createElement('button');
        btn.innerHTML = '📋 Copy';
        btn.className = 'copy-code-btn';
        
        btn.onclick = () => {
            const code = pre.querySelector('code');
            const textToCopy = code ? code.innerText : pre.innerText;
            
            navigator.clipboard.writeText(textToCopy).then(() => {
                btn.innerHTML = '✅ Copied!';
                btn.classList.add('success');
                setTimeout(() => {
                    btn.innerHTML = '📋 Copy';
                    btn.classList.remove('success');
                }, 2000);
            });
        };

        wrapper.appendChild(btn);
    });
}

/**
 * Display error messages in a consistent format
 * @param {string} msg - Error message string
 */
function showError(msg) {
    const responseElement = document.getElementById('ai-response');
    responseElement.innerHTML = `<div class="error-box">${msg}</div>`;
}

/**
 * Copies the *rendered* response text to the user's clipboard
 */
function copyToClipboard() {
    const responseElement = document.getElementById('ai-response');
    const bntCopy = document.getElementById('btn-copy');

    // Extract text content from the rendered response container
    const textToCopy = responseElement.textContent || responseElement.innerText;
    
    if (textToCopy && !textToCopy.includes("Awaiting your instruction")) {
        navigator.clipboard.writeText(textToCopy).then(() => {
            const originalLabel = bntCopy.innerHTML;
            bntCopy.innerHTML = "✅ SUCCESS!";
            bntCopy.style.borderColor = "#10b981";
            bntCopy.style.color = "#10b981";
            
            setTimeout(() => {
                bntCopy.innerHTML = originalLabel;
                bntCopy.style.borderColor = "";
                bntCopy.style.color = "";
            }, 2000);
        }).catch(err => {
            console.error('Clipboard Access Denied: ', err);
            alert('Could not access clipboard.');
        });
    } else {
        alert("Nothing to copy! Process a prompt first.");
    }
}
