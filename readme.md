
## 🎥 YouTube Video Summarization Application 🎥

Summarize YouTube videos with ease using our application powered by the BART model. 🚀

### 🌟 Features

1. **🖱️ Easy to Use**: Just input the YouTube video URL and get the summary in seconds.
2. **🧠 BART Model**: Uses the BART Large CNN model for state-of-the-art summarization.
3. **🔄 Progress Status**: Real-time updates on the summarization process.
4. **🚫 Error Handling**: Gracefully handles any errors during the summarization process.

### 📚 Model Overview

#### [🔗 Facebook BART Large CNN Model](https://huggingface.co/facebook/bart-large-cnn)

The Facebook BART Large CNN model is a popular choice for text summarization. It's a transformer model fine-tuned for text generation, including summarization. The model was introduced in a research paper by Lewis et al.

Using the Hugging Face Transformers library, you can leverage this model for text summarization. This library provides a pipeline API for various NLP tasks, including summarization.

```python
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
text = "Insert your text here"
summary = summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
print(summary)
```

While there are other methods and models for text summarization, the Facebook BART Large CNN model remains a top choice for this task.

### 🚀 Getting Started

#### 📋 Prerequisites

- Django 🌐
- Transformers 🤖
- YouTube Transcript API 🎙️

#### 🛠️ Installation

1. 📂 Clone the repository.
2. 📍 Navigate to the project directory.
3. ⚙️ Install the required packages using `pip install -r requirements.txt`.
4. 🏃 Run the Django server.

### 🖥️ Usage

1. 🌍 Navigate to the application's main page.
2. 📝 Enter the YouTube video URL in the provided input field.
3. 🎉 Click on "Summarize".
4. ⏳ Wait for the summarization to complete and view the results.

### 🔗 Endpoints

1. **🏠 Index**: Main page of the application.
2. **📜 Summarize Video**: Endpoint that takes a YouTube URL and returns the summarized content.
3. **🔍 Check Progress**: Fetch the current progress status of the summarization.

### 🎬 Behind the Scenes

The application fetches the transcript of the provided YouTube video, divides it into chunks, and processes each chunk using the BART model for a summary. The final content combines all the summarized chunks.

### ⚠️ Known Limitations

- 📏 Specific YouTube URL format required.
- ⏱️ Long videos might take more time for summarization.

### 🛤️ Future Work

- 📹 Support for more video platforms.
- 🙋 Introduction of user accounts and saved summaries.

### 🤝 Contributing

I welcome contributions! 🎉 Raise an issue or submit a pull request to improve the application.

## License 📜

This project is licensed under the [MIT License](LICENSE)
