from transformers import BartTokenizer, BartForConditionalGeneration, pipeline

MODEL_PATH = "bart_large_cnn"

# Load the model and tokenizer
model = BartForConditionalGeneration.from_pretrained(MODEL_PATH)
tokenizer = BartTokenizer.from_pretrained(MODEL_PATH)

# Display the model's vocab size
print(f"Model's vocab size: {model.config.vocab_size}")

# Check the token IDs
test_sentence = "Recognize this sound? If you pop or crack your joints, you probably do."
token_ids = tokenizer.encode(test_sentence, return_tensors="pt")
print(token_ids)
max_token_id = max(token_ids[0].tolist())
print(f"Max token ID: {max_token_id}")

# Check if max token ID is within the range
if max_token_id >= model.config.vocab_size:
    print("Warning: Max token ID exceeds the model's vocab size. There might be a mismatch.")

# Summarize the test sentence
else:
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
    summary = summarizer(test_sentence, max_length=40, min_length=10, do_sample=False)
    print(summary[0]['summary_text'])
