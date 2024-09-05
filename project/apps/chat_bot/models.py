# models.py
from django.db import models

class FAQCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class FAQ(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs')
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question
