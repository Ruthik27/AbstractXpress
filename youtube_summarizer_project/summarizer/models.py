from django.db import models

class VideoSummary(models.Model):
    video_url = models.URLField(unique=True)
    summarized_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
