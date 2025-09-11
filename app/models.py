from django.db import models
from django.utils import timezone

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_published = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='news/', blank=True, null=True)

    class Meta:
        ordering = ['-date_published']

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='events/', blank=True, null=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='faculty/', blank=True, null=True)
    bio = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Faculty"

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=20)
    description = models.TextField()
    duration = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.grade}"

class Facility(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='facilities/')

    class Meta:
        verbose_name_plural = "Facilities"

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_sent = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.subject}"