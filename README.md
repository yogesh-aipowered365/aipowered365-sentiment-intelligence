# Sentiment Analysis App

A Gradio-based sentiment analysis application powered by a fine-tuned Twitter RoBERTa model.

## Features

- **Single Text Analysis**: Analyze sentiment of individual text inputs
- **Batch Processing**: Process CSV/Excel files with bulk sentiment analysis
- **Real-time Results**: Get immediate sentiment predictions with confidence scores
- **User-Friendly Interface**: Clean and intuitive Gradio web interface

## Model

Uses the `cardiffnlp/twitter-roberta-base-sentiment-latest` model from Hugging Face Hub.

## Usage

### Local Deployment

```bash
pip install -r requirements.txt
python app.py
```

### Hugging Face Spaces

This app is deployed on [Hugging Face Spaces](https://huggingface.co/spaces) and can be accessed directly in your browser.

## Requirements

See `requirements.txt` for all dependencies.

## Author

Created with Gradio and Transformers
