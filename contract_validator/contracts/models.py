

# Create your models here.
from django.db import models

class Contract(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='contracts/')
    text = models.TextField()
    entities = models.TextField()
    highlighted_text = models.TextField()
    predicted_text = models.TextField()
    summarized_text = models.TextField()

    def __str__(self):
        return f"Contract uploaded at {self.uploaded_at}"