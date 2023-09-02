import os
import re
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from transformers import BartTokenizer, BartForConditionalGeneration
from django.shortcuts import render, redirect
from django.http import JsonResponse
import youtube_dl
from transformers import BartForConditionalGeneration, BartTokenizer, pipeline
from youtube_transcript_api import YouTubeTranscriptApi


# Constants
AUDIO_SAVE_PATH = "audio_files"
MODEL_PATH = "distilbart_model_dir"

# Setting up the summarizer
model = BartForConditionalGeneration.from_pretrained(MODEL_PATH)
tokenizer = BartTokenizer.from_pretrained(MODEL_PATH)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

# Progress status dictionary
progress_status = {
    'status': 'pending',  # can be 'pending', 'processing', 'completed', 'error'
    'progress': 0,  # a percentage (0-100)
    'message': ''
}

# Add other necessary imports here (e.g., YouTube downloader, transcription and summarization libraries, etc.)

from django.shortcuts import render

def index(request):
    """
    Render the main page for users to input the YouTube URL.
    """
    return render(request, 'summarizer/index.html')


from django.shortcuts import render, redirect
from django.http import HttpResponse
from transformers import BartForConditionalGeneration, BartTokenizer, pipeline
import youtube_dl
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_SAVE_PATH = os.path.join(BASE_DIR, 'audio_files')
MODEL_DIR = os.path.join(BASE_DIR, 'distilbart_model_dir')

# Initialize the model and tokenizer
model = BartForConditionalGeneration.from_pretrained(MODEL_DIR)
tokenizer = BartTokenizer.from_pretrained(MODEL_DIR)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

def error_template(request):
    return render(request, 'summarizer/error_template.html')


def summarize_video(request):
    try:
        if request.method == "POST":
            video_url = request.POST.get('video_url')

            # Update progress status
            progress_status['status'] = 'processing'
            progress_status['progress'] = 10
            progress_status['message'] = 'Downloading video...'

            # Download video and extract audio
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192',
                }],
                'outtmpl': AUDIO_SAVE_PATH + '/%(title)s.%(ext)s',
            }
            
            video_id = video_url.split("v=")[1].split("&")[0]

            # Fetch video title using youtube_dl
            try:
                with youtube_dl.YoutubeDL() as ydl:
                    info_dict = ydl.extract_info(video_url, download=False)
                    video_title = info_dict.get('title', None)
            except youtube_dl.utils.DownloadError as e:
                progress_status['status'] = 'error'
                progress_status['message'] = f"Error with youtube_dl: {str(e)}"
                return redirect('index')

        # Fetching the transcript using YouTubeTranscriptApi
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                content_to_summarize = " ".join([entry['text'] for entry in transcript])
            except Exception as e:
                progress_status['status'] = 'error'
                progress_status['message'] = f"Error fetching transcript: {str(e)}"
                return redirect('index')



            audio_file_path = os.path.join(AUDIO_SAVE_PATH, f"{video_title}.wav")

            # Update progress status
            progress_status['progress'] = 50
            progress_status['message'] = 'Video downloaded and audio extracted.'

            # Summarize content
            summary = summarizer(video_title, max_length=100, min_length=25, do_sample=False)
            summarized_text = summary[0]['summary_text']

            # Clean up the downloaded audio file
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)

            # Update progress status
            progress_status['status'] = 'completed'
            progress_status['progress'] = 100
            progress_status['message'] = 'Summarization completed.'

            # Pass the summarized text to the summary_result template
            return render(request, 'summarizer/summary_result.html', {'summary': summarized_text})

        else:
            return redirect('index')

    except Exception as e:
        # Update progress status for error
        progress_status['status'] = 'error'
        progress_status['message'] = str(e)
        return redirect('index')


def check_progress(request):
    """
    Check the progress of video summarization.
    Returns a JSON response with the current progress status.
    """
    return JsonResponse(progress_status)

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Convert the transcript into a single block of text
        full_transcript = " ".join([entry['text'] for entry in transcript])
        return full_transcript
    except:
        return None



def extract_audio(video_url, save_path="audio_files"):
    """
    Extract audio from YouTube video.
    Returns the path of the extracted audio file.
    """
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': save_path + '/%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        info_dict = ydl.extract_info(video_url, download=False)
        video_title = info_dict.get('title', None)
    
    return os.path.join(save_path, f"{video_title}.wav")

def transcribe_audio(audio_file_path):
    """
    Transcribes audio to text.
    Here, as a placeholder, we return the file name as the transcription.
    In a real-world scenario, use a transcription service or model.
    """
    
    return os.path.basename(audio_file_path).replace(".wav", "")


from transformers import BartForConditionalGeneration, BartTokenizer, pipeline

# Assuming you've already loaded the model and tokenizer as shown before
model_path = "distilbart_model_dir"
model = BartForConditionalGeneration.from_pretrained(model_path)
tokenizer = BartTokenizer.from_pretrained(model_path)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

def summarize_text(text):
    """
    Summarizes the provided text using DistilBART.
    Returns the summarized text.
    """
    
    summary = summarizer(text, max_length=100, min_length=25, do_sample=False)
    return summary[0]['summary_text']


