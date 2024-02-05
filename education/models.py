from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    context = models.TextField()
    question_text = models.TextField()
    rubric = models.TextField()  # For evaluation

class StudentResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student_answer = models.TextField()
    evaluation = models.TextField()  # AI-generated feedback
    score = models.FloatField()  # AI-generated score

