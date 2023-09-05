import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from transformers import BartTokenizer, BartForConditionalGeneration, pipeline
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import PreTrainedTokenizerFast


# Constants
AUDIO_SAVE_PATH = "audio_files"
MODEL_PATH = "bart_large_cnn"  # Local directory

# Load the model and tokenizer
model = BartForConditionalGeneration.from_pretrained(MODEL_PATH)
tokenizer = BartTokenizer.from_pretrained(MODEL_PATH)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

# Progress status dictionary
progress_status = {
    'status': 'pending',
    'progress': 0,
    'message': 'Initializing...'
}

def index(request):
    return render(request, 'summarizer/index.html')

def summarize_video(request):
    try:
        if request.method == "POST":
            video_url = request.POST.get('video_url')
            print("URL to be parsed:", video_url)

            # Extract video ID from the URL
            try:
                video_id = video_url.split("v=")[1].split("&")[0]
            except IndexError:
                progress_status['status'] = 'error'
                progress_status['message'] = 'Invalid YouTube URL provided.'
                return redirect('index')


            # Fetching the transcript using YouTubeTranscriptApi
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                progress_status['progress'] = 25
                progress_status['message'] = 'Transcript extracted. Summarizing...'
            except Exception as e:
                progress_status['status'] = 'error'
                progress_status['message'] = f"An error occurred while fetching transcript: {str(e)}"
                return redirect('index')

            content_to_summarize = " ".join([entry['text'] for entry in transcript])

            # Summarize content
            # Summarize content using the summarize_large_text function
            summarized_text = summarize_large_text(content_to_summarize)


            # Update progress status
            progress_status['progress'] = 100
            progress_status['message'] = 'Summarization completed.'

            return render(request, 'summarizer/summary_result.html', {'summary': summarized_text})

        else:
            return redirect('index')

    except Exception as e:
        # Update progress status for error
        progress_status['status'] = 'error'
        progress_status['message'] = str(e)
        return redirect('index')

def check_progress(request):
    return JsonResponse(progress_status)

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        print(transcript)
        full_transcript = " ".join([entry['text'] for entry in transcript])
        return full_transcript
    except:
        return None

def chunk_text(text, max_length=1024):
    """Split the text into chunks of max_length."""
    sentences = text.split('.')
    chunks = []

    current_chunk = ""
    for sentence in sentences:
        if len(tokenizer.tokenize(current_chunk + sentence)) < max_length:
            current_chunk += sentence + "."
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + "."
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def summarize_large_text(text):
    """Summarize text that is longer than the model's maximum input length."""
    try:
        # 1. Test Summarizer with a Short Sentence
        test_sentence = "Recognize this sound? If you pop or crack your joints, you probably do."
        
        token_count = len(tokenizer.tokenize(test_sentence))
        print("Token count for test sentence:", token_count)

        adjusted_max_length = min(50, token_count + 5)  # Adjusting the max_length for the test sentence
        test_summary = summarizer(test_sentence, max_length=adjusted_max_length, min_length=10, do_sample=False)
        print("Test Summary:", test_summary[0]['summary_text'])
        
        # 2. Chunking the text
        chunks = chunk_text(text)
        progress_increment = 50 / len(chunks)  # Calculate progress increment based on the number of chunks

        all_summaries = []

        for current_chunk_text in chunks:
            # If the chunk is empty, continue to the next chunk
            if not current_chunk_text.strip():
                continue

            token_count_chunk = len(tokenizer.tokenize(current_chunk_text))
            print("Token count for current chunk:", token_count_chunk)

            # Ensure the token count is within the model's limit (e.g., 1024 for BERT-based models)
            if token_count_chunk > 1024:
                print("Token count exceeds model's limit. Skipping this chunk.")
                continue

            current_max_length = min(token_count_chunk + 20, 100)  # Adjusting the max_length
            print("Chunk being summarized:", current_chunk_text)
            summary = summarizer(current_chunk_text, max_length=current_max_length, min_length=25, do_sample=False)
            all_summaries.append(summary[0]['summary_text'])

            # Update progress after summarizing the chunk
            progress_status['progress'] += progress_increment
            progress_status['message'] = f'Summarized {round(progress_status["progress"])}% of the content...'

        
        return " ".join(all_summaries)

    except Exception as e:
        print("Error during summarization:", str(e))
        return "Error during summarization: " + str(e)



def summarize_text(text):
    # Summarize content
    summarized_text = summarize_large_text(text)
    return summarized_text

