from flask import Flask, request, jsonify, render_template_string
import re
import os

app = Flask(__name__)

# Simple text summarization function (no ML models needed)
def simple_summarize(text, max_length=150):
    """Simple extractive summarization using sentence scoring"""
    # Clean the text
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return "No text to summarize."
    
    # Simple scoring based on word frequency
    word_freq = {}
    for sentence in sentences:
        words = re.findall(r'\b\w+\b', sentence.lower())
        for word in words:
            if len(word) > 3:  # Skip short words
                word_freq[word] = word_freq.get(word, 0) + 1
    
    # Score sentences
    sentence_scores = []
    for sentence in sentences:
        words = re.findall(r'\b\w+\b', sentence.lower())
        score = sum(word_freq.get(word, 0) for word in words if len(word) > 3)
        sentence_scores.append((score, sentence))
    
    # Sort by score and take top sentences
    sentence_scores.sort(reverse=True)
    
    summary = ""
    for score, sentence in sentence_scores:
        if len(summary + sentence) <= max_length:
            summary += sentence + ". "
        else:
            break
    
    return summary.strip() if summary else sentences[0] + "."

# Load the summarizer
print("Loading simple summarizer...")
print("Simple summarizer loaded successfully!")

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Text Summarizer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #6366f1;
            --primary-dark: #4f46e5;
            --secondary-color: #8b5cf6;
            --success-color: #10b981;
            --error-color: #ef4444;
            --warning-color: #f59e0b;
            --text-primary: #1f2937;
            --text-secondary: #6b7280;
            --bg-primary: #ffffff;
            --bg-secondary: #f9fafb;
            --bg-tertiary: #f3f4f6;
            --border-color: #e5e7eb;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }

        [data-theme="dark"] {
            --text-primary: #f9fafb;
            --text-secondary: #d1d5db;
            --bg-primary: #111827;
            --bg-secondary: #1f2937;
            --bg-tertiary: #374151;
            --border-color: #4b5563;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
            transition: all 0.3s ease;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        .header {
            text-align: center;
            margin-bottom: 3rem;
            position: relative;
        }

        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
            animation: fadeInUp 0.8s ease-out;
        }

        .header p {
            font-size: 1.2rem;
            color: var(--text-secondary);
            margin-bottom: 2rem;
            animation: fadeInUp 0.8s ease-out 0.2s both;
        }

        .theme-toggle {
            position: absolute;
            top: 0;
            right: 0;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 50px;
            padding: 0.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            animation: fadeInUp 0.8s ease-out 0.4s both;
        }

        .theme-toggle:hover {
            transform: scale(1.05);
            box-shadow: var(--shadow-md);
        }

        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3rem;
            margin-bottom: 3rem;
            animation: fadeInUp 0.8s ease-out 0.6s both;
        }

        .input-section, .output-section {
            background: var(--bg-primary);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: var(--shadow-xl);
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }

        .input-section:hover, .output-section:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-xl), 0 0 0 1px var(--primary-color);
        }

        .section-header {
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .section-header i {
            margin-right: 0.75rem;
            color: var(--primary-color);
            font-size: 1.25rem;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: var(--text-primary);
            font-size: 0.95rem;
        }

        textarea {
            width: 100%;
            min-height: 300px;
            padding: 1rem;
            border: 2px solid var(--border-color);
            border-radius: 12px;
            font-size: 1rem;
            font-family: inherit;
            resize: vertical;
            background: var(--bg-secondary);
            color: var(--text-primary);
            transition: all 0.3s ease;
        }

        textarea:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        .btn {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 1rem 2rem;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }

        .btn:active {
            transform: translateY(0);
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .loading {
            display: none;
            text-align: center;
            margin: 2rem 0;
        }

        .spinner {
            border: 3px solid var(--border-color);
            border-top: 3px solid var(--primary-color);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .result {
            display: none;
            margin-top: 2rem;
        }

        .success, .error {
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }

        .success {
            background: linear-gradient(135deg, var(--success-color), #059669);
            color: white;
        }

        .error {
            background: linear-gradient(135deg, var(--error-color), #dc2626);
            color: white;
        }

        .result-content h3 {
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            font-size: 1.25rem;
        }

        .result-content h3 i {
            margin-right: 0.5rem;
        }

        .summary-text {
            background: rgba(255, 255, 255, 0.1);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            line-height: 1.6;
            font-size: 1.1rem;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-top: 1.5rem;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
        }

        .stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }

        .stat-label {
            font-size: 0.875rem;
            opacity: 0.9;
        }

        .placeholder {
            text-align: center;
            color: var(--text-secondary);
            font-style: italic;
            margin: 2rem 0;
        }

        .api-docs {
            background: var(--bg-primary);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: var(--shadow-xl);
            border: 1px solid var(--border-color);
            margin-top: 3rem;
        }

        .api-section {
            margin-bottom: 2rem;
        }

        .api-section h4 {
            color: var(--text-primary);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
        }

        .api-section h4 i {
            margin-right: 0.5rem;
            color: var(--primary-color);
        }

        pre {
            background: var(--bg-secondary);
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 0.875rem;
            border: 1px solid var(--border-color);
        }

        .health-link {
            display: inline-flex;
            align-items: center;
            color: var(--primary-color);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .health-link:hover {
            color: var(--primary-dark);
        }

        .health-link i {
            margin-left: 0.5rem;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .particle {
            position: absolute;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            border-radius: 50%;
            opacity: 0.1;
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% {
                transform: translateY(0px) rotate(0deg);
                opacity: 0.1;
            }
            50% {
                transform: translateY(-20px) rotate(180deg);
                opacity: 0.3;
            }
        }

        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
                gap: 2rem;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .stats {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div id="particles"></div>
    
    <div class="container">
        <div class="header">
            <h1>AI Text Summarizer</h1>
            <p>Transform long text into concise, meaningful summaries with our intelligent summarization tool</p>
            <button class="theme-toggle" onclick="toggleTheme()">
                <i id="theme-icon" class="fas fa-moon"></i>
            </button>
        </div>

        <div class="main-content">
            <div class="input-section">
                <div class="section-header">
                    <i class="fas fa-edit"></i>
                    Input Text
                </div>
                <form id="summarizeForm">
                    <div class="form-group">
                        <label for="text">Enter your text to summarize:</label>
                        <textarea id="text" name="text" placeholder="Paste your text here... (minimum 50 characters)" required></textarea>
                    </div>
                    <button type="submit" class="btn" id="submitBtn">
                        <i class="fas fa-magic"></i>
                        Generate Summary
                    </button>
                </form>
            </div>

            <div class="output-section">
                <div class="section-header">
                    <i class="fas fa-chart-line"></i>
                    Summary Results
                </div>
                
                <div id="loading" class="loading">
                    <div class="spinner"></div>
                    <p>Generating your summary...</p>
                </div>
                
                <div id="placeholder" class="placeholder">
                    <i class="fas fa-arrow-left" style="font-size: 2rem; margin-bottom: 1rem; display: block; color: var(--text-secondary);"></i>
                    Enter text on the left and click "Generate Summary" to see results here
                </div>
                
                <div id="result" class="result"></div>
            </div>
        </div>

        <div class="api-docs">
            <h3 style="margin-bottom: 2rem; color: var(--text-primary);">
                <i class="fas fa-code"></i>
                API Documentation
            </h3>
            
            <div class="api-section">
                <h4><i class="fas fa-paper-plane"></i> Summarize Text</h4>
                <pre>POST /summarize
Content-Type: application/json

{
  "text": "Your text to summarize here..."
}</pre>
            </div>
            
            <div class="api-section">
                <h4><i class="fas fa-download"></i> Response Format</h4>
                <pre>{
  "original_text": "...",
  "summary": "...",
  "original_length": 123,
  "summary_length": 45
}</pre>
            </div>
            
            <div class="api-section">
                <h4><i class="fas fa-heartbeat"></i> Health Check</h4>
                <a href="/health" target="_blank" class="health-link">
                    GET /health
                    <i class="fas fa-external-link-alt"></i>
                </a>
            </div>
        </div>
    </div>

    <script>
        // Theme toggle functionality
        function toggleTheme() {
            const body = document.body;
            const themeIcon = document.getElementById('theme-icon');
            
            if (body.getAttribute('data-theme') === 'dark') {
                body.removeAttribute('data-theme');
                themeIcon.className = 'fas fa-moon';
                localStorage.setItem('theme', 'light');
            } else {
                body.setAttribute('data-theme', 'dark');
                themeIcon.className = 'fas fa-sun';
                localStorage.setItem('theme', 'dark');
            }
        }

        // Load saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.setAttribute('data-theme', 'dark');
            document.getElementById('theme-icon').className = 'fas fa-sun';
        }

        // Create floating particles
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            for (let i = 0; i < 20; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.width = Math.random() * 10 + 5 + 'px';
                particle.style.height = particle.style.width;
                particle.style.animationDelay = Math.random() * 6 + 's';
                particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
                particlesContainer.appendChild(particle);
            }
        }

        // Initialize particles
        createParticles();

        // Form submission
        document.getElementById('summarizeForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const text = document.getElementById('text').value.trim();
            if (!text) {
                showNotification('Please enter some text to summarize', 'error');
                return;
            }
            
            const submitBtn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const placeholder = document.getElementById('placeholder');
            
            // Show loading
            submitBtn.disabled = true;
            loading.style.display = 'block';
            result.style.display = 'none';
            placeholder.style.display = 'none';
            
            try {
                const response = await fetch('/summarize', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: text })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    const compressionRatio = ((data.summary_length / data.original_length) * 100).toFixed(1);
                    const wordsOriginal = data.original_text.split(' ').length;
                    const wordsSummary = data.summary.split(' ').length;
                    
                    result.innerHTML = `
                        <div class="success">
                            <div class="result-content">
                                <h3><i class="fas fa-check-circle"></i> Summary Generated Successfully!</h3>
                                <div class="summary-text">${data.summary}</div>
                                <div class="stats">
                                    <div class="stat-card">
                                        <div class="stat-value">${data.original_length}</div>
                                        <div class="stat-label">Original Characters</div>
                                    </div>
                                    <div class="stat-card">
                                        <div class="stat-value">${data.summary_length}</div>
                                        <div class="stat-label">Summary Characters</div>
                                    </div>
                                    <div class="stat-card">
                                        <div class="stat-value">${compressionRatio}%</div>
                                        <div class="stat-label">Compression Ratio</div>
                                    </div>
                                    <div class="stat-card">
                                        <div class="stat-value">${wordsOriginal}</div>
                                        <div class="stat-label">Original Words</div>
                                    </div>
                                    <div class="stat-card">
                                        <div class="stat-value">${wordsSummary}</div>
                                        <div class="stat-label">Summary Words</div>
                                    </div>
                                    <div class="stat-card">
                                        <div class="stat-value">${((wordsSummary / wordsOriginal) * 100).toFixed(1)}%</div>
                                        <div class="stat-label">Word Reduction</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                } else {
                    result.innerHTML = `
                        <div class="error">
                            <div class="result-content">
                                <h3><i class="fas fa-exclamation-triangle"></i> Error</h3>
                                <p>${data.error || 'An error occurred while generating the summary'}</p>
                            </div>
                        </div>
                    `;
                }
            } catch (error) {
                result.innerHTML = `
                    <div class="error">
                        <div class="result-content">
                            <h3><i class="fas fa-exclamation-triangle"></i> Connection Error</h3>
                            <p>Failed to connect to the API. Please check your internet connection and try again.</p>
                        </div>
                    </div>
                `;
            } finally {
                // Hide loading
                submitBtn.disabled = false;
                loading.style.display = 'none';
                result.style.display = 'block';
            }
        });

        // Show notification function
        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 1rem 1.5rem;
                border-radius: 8px;
                color: white;
                font-weight: 500;
                z-index: 1000;
                animation: slideInRight 0.3s ease-out;
                max-width: 300px;
            `;
            
            if (type === 'error') {
                notification.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
            } else {
                notification.style.background = 'linear-gradient(135deg, #10b981, #059669)';
            }
            
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
        }

        // Add slideInRight animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(100%);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        # Get the text from the request
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Generate summary
        summary = simple_summarize(text)
        
        if not summary:
            return jsonify({'error': 'Generated summary is empty'}), 500
        
        return jsonify({
            'original_text': text,
            'summary': summary,
            'original_length': len(text),
            'summary_length': len(summary)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'API is running'})

if __name__ == '__main__':
    print("Starting Flask API...")
    print("Visit http://localhost:5000 for the web interface")
    app.run(host='0.0.0.0', port=5000, debug=True)