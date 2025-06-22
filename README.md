# 🤖 AI Text Summarizer

A beautiful, modern web application that uses advanced AI to transform long text into concise, meaningful summaries. Built with Flask, Transformers, and a stunning responsive UI.

![AI Text Summarizer](https://img.shields.io/badge/AI-Text%20Summarizer-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-green?style=for-the-badge&logo=flask)
![Transformers](https://img.shields.io/badge/Transformers-Hugging%20Face-orange?style=for-the-badge&logo=huggingface)
![Railway](https://img.shields.io/badge/Deploy%20on-Railway-0B0D0E?style=for-the-badge&logo=railway)

## ✨ Features

### 🎨 Beautiful Modern UI
- **Gradient Design**: Stunning purple-to-blue gradients
- **Dark/Light Mode**: Toggle between themes with persistent preferences
- **Floating Particles**: Subtle animated background elements
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile
- **Smooth Animations**: Professional fade-in effects and hover transitions
- **Modern Typography**: Clean Inter font throughout the interface

### 🤖 Advanced AI Summarization
- **Pegasus Model**: Uses Google's state-of-the-art Pegasus model
- **Smart Compression**: Intelligent text reduction while preserving key information
- **Detailed Statistics**: Character count, word count, compression ratios
- **Real-time Processing**: Fast, efficient summarization

### 🛠️ Technical Features
- **RESTful API**: Clean API endpoints for programmatic access
- **Health Monitoring**: Built-in health check endpoint
- **Error Handling**: Comprehensive error handling and user feedback
- **Production Ready**: Optimized for deployment with Gunicorn

## 🚀 Live Demo

Visit the live application: [AI Text Summarizer](https://your-railway-app.railway.app)

## 📋 Prerequisites

- Python 3.8+
- pip package manager
- Git

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/text-summarization-nlp-project.git
   cd text-summarization-nlp-project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python simple_app.py
   ```

5. **Open your browser**
   Visit `http://localhost:5000`

## 🎯 Usage

### Web Interface
1. Open the application in your browser
2. Paste or type your text in the input area
3. Click "Generate Summary"
4. View the beautiful summary with detailed statistics

### API Usage
```bash
# Health check
curl https://your-app.railway.app/health

# Summarize text
curl -X POST https://your-app.railway.app/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text to summarize here..."}'
```

## 🏗️ Project Structure

```
Text-Summarization-NLP-Project/
├── simple_app.py          # Main Flask application
├── requirements.txt       # Python dependencies
├── railway.json          # Railway deployment config
├── Procfile             # Railway process file
├── runtime.txt          # Python version specification
├── .railwayignore       # Files to exclude from deployment
├── README.md            # This file
├── artifacts/           # Model artifacts (not deployed)
├── src/                 # Source code
└── config/              # Configuration files
```

## 🚀 Deployment

### Railway Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Railway deployment configuration"
   git push origin main
   ```

2. **Deploy on Railway**
   - Go to [Railway.app](https://railway.app)
   - Sign in with your GitHub account
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will automatically detect the Flask app and deploy it

3. **Environment Variables** (if needed)
   - Railway will automatically set the `PORT` environment variable
   - Add any additional environment variables in the Railway dashboard

### Alternative Deployment Options

- **Heroku**: Use the Procfile and requirements.txt
- **Docker**: Build and deploy using Docker containers
- **VPS**: Deploy directly to a virtual private server

## 🔧 Configuration

### Environment Variables
- `PORT`: Port number (set automatically by Railway)
- `FLASK_ENV`: Set to `production` for production deployment

### Model Configuration
The application uses the Google Pegasus model by default. You can modify the model in `simple_app.py`:

```python
summarizer = pipeline("summarization", model="google/pegasus-cnn_dailymail")
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 📊 API Documentation

### Endpoints

#### `GET /`
- **Description**: Web interface
- **Response**: HTML page with the beautiful UI

#### `GET /health`
- **Description**: Health check endpoint
- **Response**: JSON with status information
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

#### `POST /summarize`
- **Description**: Summarize text
- **Request Body**:
```json
{
  "text": "Your text to summarize..."
}
```
- **Response**:
```json
{
  "original_text": "...",
  "summary": "...",
  "original_length": 123,
  "summary_length": 45
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/transformers/) for the AI models
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Railway](https://railway.app/) for the deployment platform
- [Font Awesome](https://fontawesome.com/) for the beautiful icons

## 📞 Support

If you have any questions or need help, please open an issue on GitHub or contact the maintainers.

---

⭐ **Star this repository if you found it helpful!** 