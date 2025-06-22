from flask import Flask, request, jsonify, render_template_string
import re
import os

app = Flask(__name__)

def simple_summarize(text, max_length=150):
    text = re.sub(r'\s+', ' ', text).strip()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return "No text to summarize."

    word_freq = {}
    for sentence in sentences:
        words = re.findall(r'\b\w+\b', sentence.lower())
        for word in words:
            if len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1

    sentence_scores = []
    for sentence in sentences:
        words = re.findall(r'\b\w+\b', sentence.lower())
        score = sum(word_freq.get(word, 0) for word in words if len(word) > 3)
        sentence_scores.append((score, sentence))

    sentence_scores.sort(reverse=True)

    summary = ""
    for score, sentence in sentence_scores:
        if len(summary + sentence) <= max_length:
            summary += sentence + ". "
        else:
            break

    return summary.strip() if summary else sentences[0] + "."

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>QuickText Summary Tool</title>
    <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap\" rel=\"stylesheet\">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f9fafb;
            color: #1f2937;
            margin: 0;
            padding: 2rem;
        }

        h1 {
            font-size: 2.5rem;
            color: #4f46e5;
            text-align: center;
        }

        p.description {
            text-align: center;
            color: #6b7280;
            margin-bottom: 2rem;
        }

        .container {
            max-width: 700px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        textarea {
            width: 100%;
            padding: 1rem;
            font-size: 1rem;
            border: 1px solid #d1d5db;
            border-radius: 0.75rem;
            resize: vertical;
        }

        .btn {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            padding: 1.2rem;
            border: none;
            border-radius: 9999px;
            cursor: pointer;
            font-size: 1.1rem;
            font-weight: 700;
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
            transition: all 0.3s ease;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(139, 92, 246, 0.4);
        }

        .output {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 1rem;
            border: 1px solid #e5e7eb;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }

        .stats {
            margin-top: 1rem;
            font-size: 0.95rem;
            color: #4b5563;
        }
    </style>
</head>
<body>
    <h1>QuickText Summary Tool</h1>
    <p class=\"description\">Simplify any long text into a short and smart summary</p>
    <div class=\"container\">
        <form method=\"post\">
            <textarea name=\"text\" rows=\"10\" placeholder=\"Paste your text here...\" required>{{ original_text }}</textarea>
            <button class=\"btn\" type=\"submit\">&#x2728; Generate Summary</button>
        </form>
        {% if summary %}
        <div class=\"output\">
            <h3>Summary:</h3>
            <p>{{ summary }}</p>
            <div class=\"stats\">
                <p><strong>Original Word Count:</strong> {{ original_word_count }}</p>
                <p><strong>Summary Word Count:</strong> {{ summary_word_count }}</p>
                <p><strong>Reduction:</strong> {{ reduction_percent }}%</p>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    summary = None
    original_text = ''
    original_word_count = 0
    summary_word_count = 0
    reduction_percent = 0
    if request.method == 'POST':
        original_text = request.form.get('text', '')
        if original_text:
            summary = simple_summarize(original_text)
            original_word_count = len(original_text.split())
            summary_word_count = len(summary.split())
            if original_word_count > 0:
                reduction_percent = round(100 - (summary_word_count / original_word_count * 100), 2)
    return render_template_string(
        HTML_TEMPLATE,
        summary=summary,
        original_text=original_text,
        original_word_count=original_word_count,
        summary_word_count=summary_word_count,
        reduction_percent=reduction_percent
    )

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        text = data.get('text', '')
        if not text:
            return jsonify({'error': 'No text provided'}), 400
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
