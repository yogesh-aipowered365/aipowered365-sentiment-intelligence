# Sentiment Analysis App

<div align="center">
  <img src="logo.png" alt="AIpowered365 Logo" width="200" height="200">
  
  **Mastering Dynamics 365 & AI Innovations**
</div>

> A production-ready Gradio web application for real-time sentiment analysis powered by advanced NLP models.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Gradio](https://img.shields.io/badge/Gradio-6.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

## 🎯 Overview

AIpowered365 Sentiment Intelligence is a comprehensive sentiment analysis solution that classifies text into **Positive**, **Negative**, or **Neutral** categories. Perfect for customer feedback analysis, social media monitoring, and content moderation.

### Key Features

- ✨ **Single Text Analysis** - Analyze individual messages with confidence scores and explanations
- 📊 **Batch Processing** - Process CSV/Excel files with thousands of texts simultaneously
- ⚡ **Real-time Results** - Instant sentiment predictions with detailed explanations
- 🎨 **Professional UI** - Clean, responsive Gradio interface with custom styling
- 🚀 **Production Ready** - Deployed on Hugging Face Spaces for easy access
- 💼 **Enterprise Ready** - Available for API integration and custom deployments

## 🏗️ Architecture

```
sentiment-app/
├── app.py              # Main Gradio application
├── model.py            # Sentiment analysis model wrapper
├── config.py           # Configuration and business info
├── requirements.txt    # Python dependencies
├── theme.css           # Custom styling
├── LICENSE             # MIT License
├── CONTRIBUTING.md     # Contribution guidelines
└── README.md           # This file
```

## 🤖 Model Details

**Model**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Architecture**: RoBERTa-base fine-tuned on Twitter data
- **Task**: Sentiment Classification (3-class: Positive, Negative, Neutral)
- **Accuracy**: ~77% on Twitter dataset
- **Source**: [Hugging Face Hub](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest)

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip or UV package manager

### Setup (Local Development)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yogesh-aipowered365/sentiment-app.git
   cd sentiment-app
   ```

2. **Create virtual environment**
   ```bash
   # Using venv
   python -m venv .venv
   
   # Activate (Windows)
   .venv\Scripts\activate
   
   # Activate (macOS/Linux)
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the app**
   - Open browser to `http://localhost:7860`

## 🚀 Deployment

### Hugging Face Spaces (Recommended - Free)

Visit: [AIpowered365 Sentiment App]) *((https://huggingface.co/spaces/Yogeshaipowered365/Sentiment-Intelligence-app)*

**No setup required** - Just open and start analyzing!

### Local Deployment

```bash
python app.py
```

The app will launch on `http://localhost:7860`

## 💡 Usage Examples

### Single Text Analysis

1. Navigate to "Single Sentiment" tab
2. Enter your text (sentence, email, review, etc.)
3. Click "Analyze Sentiment"
4. Get instant results with confidence score and explanation

### Batch Processing (CSV/Excel)

1. Navigate to "Batch Sentiment" tab
2. Upload CSV or Excel file
3. Specify the column name containing text
4. Click "Run Batch Sentiment"
5. Download results as CSV or Excel

**Supported Formats**: `.csv`, `.xlsx`, `.xls`

## 📋 API & Premium Services

### 🔌 API Access
- Integrate sentiment analysis into your applications
- Pay-per-use or tiered pricing
- Contact: contact@aipowered365.com

### 🌟 Premium Features
- Advanced analytics and custom models
- Priority support
- Batch processing at scale
- Starting at $99/month

### 🏢 Enterprise & B2B
- Custom solutions and on-premise deployment
- Dedicated support and SLA guarantees
- Contact for pricing

📧 **Get in Touch:**
- Email: [contact@aipowered365.com](mailto:contact@aipowered365.com)
- Phone: +44 (0) 7446893391
- WhatsApp: [+44 (0) 7446893391](https://wa.me/4474468933391)
- Website: [https://aipowered365.com/](https://aipowered365.com/)
- LinkedIn: [Yogesh Kumar Patel](https://www.linkedin.com/in/yogeshkumar-patel-568365127)

## 🛠️ Configuration

Edit `config.py` to customize contact information and business offerings.

## 📊 Project Settings

In `app.py`, adjust:

```python
CASE_INSENSITIVE_COLUMN_MATCH = True
MAX_PREVIEW_ROWS = 20
BATCH_SIZE = 1000
```

## 📚 Dependencies

Key packages:
- **gradio** - Web UI framework
- **transformers** - NLP models and tokenizers
- **torch** - Deep learning framework
- **pandas** - Data processing
- **numpy** - Numerical computing

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

**Open Source with Premium Services** - Use the code freely, but commercial API access and premium features are available for enterprise clients.

## 🙋 Support

- **Issues**: Open an issue on GitHub
- **Questions**: Email contact@aipowered365.com
- **Documentation**: See [DEPLOYMENT_REPORT.md](DEPLOYMENT_REPORT.md)

## 🙏 Acknowledgments

- [Cardiff NLP](https://cardiff-nlp.github.io/) for the sentiment model
- [Hugging Face](https://huggingface.co/) for model hosting
- [Gradio](https://gradio.app/) for the web framework

---

**Made with ❤️ by AIpowered365**

Last Updated: December 2025
