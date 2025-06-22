from flask import Flask, request, jsonify, render_template_string
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers.pipelines import pipeline
import os
app = Flask(__name__)
# Load the model once when the app starts
print("Loading model...")
# Use the default model for reliable summarization
print("Loading default model for reliable performance...")
summarizer = pipeline("summarization", model="google/pegasus-cnn_dailymail")
print("Model loaded successfully!")
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
        .btn i {
            margin-right: 0.5rem;
        }
        .loading {
            text-align: center;
            padding: 2rem;
            color: var(--text-secondary);
            display: none;
        }
        .loading i {
            font-size: 2rem;
            color: var(--primary-color);
            animation: spin 1s linear infinite;
            margin-bottom: 1rem;
        }
        .result {
            margin-top: 1.5rem;
            border-radius: 12px;
            overflow: hidden;
            display: none;
            animation: slideIn 0.5s ease-out;
        }
        .success {
            background: linear-gradient(135deg, #d1fae5, #a7f3d0);
            border: 1px solid #10b981;
            color: #065f46;
        }
        .error {
            background: linear-gradient(135deg, #fee2e2, #fecaca);
            border: 1px solid #ef4444;
            color: #991b1b;
        }
        .result-content {
            padding: 1.5rem;
        }
        .result h3 {
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
        }
        .result h3 i {
            margin-right: 0.5rem;
        }
        .summary-text {
            background: rgba(255, 255, 255, 0.7);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            line-height: 1.7;
            font-size: 1.1rem;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-top: 1.5rem;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.8);
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            border: 1px solid rgba(0, 0, 0, 0.1);
        }
        .stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 0.25rem;
        }
        .stat-label {
            font-size: 0.875rem;
            color: var(--text-secondary);
            font-weight: 500;
        }
        .api-info {
            background: var(--bg-primary);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: var(--shadow-lg);
            border: 1px solid var(--border-color);
            margin-top: 3rem;
            animation: fadeInUp 0.8s ease-out 0.8s both;
        }
        .api-info h3 {
            color: var(--primary-color);
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
        }
        .api-info h3 i {
            margin-right: 0.75rem;
        }
        .api-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }
        .api-section {
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid var(--border-color);
        }
        .api-section h4 {
            color: var(--text-primary);
            margin-bottom: 1rem;
            font-size: 1.1rem;
        }
        pre {
            background: var(--bg-tertiary);
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 0.875rem;
            border: 1px solid var(--border-color);
            color: var(--text-primary);
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
            transform: translateX(5px);
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
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            .main-content {
                grid-template-columns: 1fr;
                gap: 2rem;
            }
            .header h1 {
                font-size: 2rem;
            }
            .theme-toggle {
                position: static;
                margin: 0 auto 1rem;
            }
        }
        .floating-particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }
        .particle {
            position: absolute;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            border-radius: 50%;
            opacity: 0.1;
            animation: float 6s ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
    </style>
</head>
<body>
    <div class="floating-particles" id="particles"></div>
    <div class="container">
        <div class="header">
            <button class="theme-toggle" onclick="toggleTheme()" title="Toggle dark mode">
                <i class="fas fa-moon" id="theme-icon"></i>
            </button>
            <h1><i class="fas fa-magic"></i> AI Text Summarizer</h1>
            <p>Transform long text into concise, meaningful summaries using advanced AI</p>
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
                        <textarea 
                            id="text" 
                            name="text" 
                            placeholder="Paste your article, document, or any text you'd like to summarize here. The AI will generate a concise summary while preserving the key information..."
                            required
                        ></textarea>
                    </div>
                    <button type="submit" id="submitBtn" class="btn">
                        <i class="fas fa-magic"></i>
                        Generate Summary
                    </button>
                </form>
                <div id="loading" class="loading">
                    <i class="fas fa-spinner"></i>
                    <p>Processing your text with AI...</p>
                    <p style="font-size: 0.9rem; margin-top: 0.5rem;">This may take a few moments</p>
                </div>
            </div>
            <div class="output-section">
                <div class="section-header">
                    <i class="fas fa-file-alt"></i>
                    Summary Result
                </div>
                <div id="result" class="result"></div>
                <div id="placeholder" style="text-align: center; color: var(--text-secondary); padding: 2rem;">
                    <i class="fas fa-arrow-left" style="font-size: 2rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                    <p>Enter text on the left and click "Generate Summary" to see results here</p>
                </div>
            </div>
        </div>
        <div class="api-info">
            <h3><i class="fas fa-code"></i> API Documentation</h3>
            <div class="api-grid">
                <div class="api-section">
                    <h4><i class="fas fa-link"></i> Endpoint</h4>
                    <p><strong>POST</strong> /summarize</p>
                    <p><strong>Content-Type:</strong> application/json</p>
                </div>
                <div class="api-section">
                    <h4><i class="fas fa-upload"></i> Request Format</h4>
                    <pre>{
  "text": "Your text here"
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
        result = summarizer(text, max_length=100, min_length=30)
        # Handle different possible return types from the pipeline
        if isinstance(result, list) and len(result) > 0:
            summary = result[0].get('summary_text', '')
        elif isinstance(result, dict):
            summary = result.get('summary_text', '')
        else:
            return jsonify({'error': 'Failed to generate summary'}), 500
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
