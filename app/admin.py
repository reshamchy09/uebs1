from django.contrib import admin
from .models import News, Event, Faculty, Course, Facility, Contact

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_published']
    list_filter = ['date_published']
    search_fields = ['title', 'content']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location']
    list_filter = ['date']
    search_fields = ['title', 'description']

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'subject', 'email']
    list_filter = ['designation', 'subject']
    search_fields = ['name', 'subject']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', 'duration']
    list_filter = ['grade']
    search_fields = ['name', 'description']

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'date_sent']
    list_filter = ['date_sent']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['date_sent']