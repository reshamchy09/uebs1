from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import News, Event, Faculty, Course, Facility, Contact
from .forms import ContactForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .firebase_config import FIREBASE_CONFIG
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import xlsxwriter
import os
from django.http import Http404
from django.conf import settings
import json

def home(request):
    latest_news = News.objects.all()[:5]
    upcoming_events = Event.objects.all()[:3]
    context = {
        'latest_news': latest_news,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def academics(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'academics.html', context)

def admissions(request):
    return render(request, 'admissions.html')

def learning(request):
    return render(request, 'e-learning.html')

def error(request):
    return render(request, '404.html')

def support(request):
    return render(request, 'admin_help_support.html')

def facilities(request):
    facilities = Facility.objects.all()
    context = {'facilities': facilities}
    return render(request, 'facilities.html', context)

def events(request):
    events_list = Event.objects.all()
    paginator = Paginator(events_list, 6)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)
    
    news_list = News.objects.all()
    news_paginator = Paginator(news_list, 6)
    news_page = request.GET.get('news_page')
    news = news_paginator.get_page(news_page)
    
    context = {
        'events': events,
        'news': news,
    }
    return render(request, 'events.html', context)

def faculty(request):
    faculty_members = Faculty.objects.all()
    context = {'faculty_members': faculty_members}
    return render(request, 'faculty.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, 'contact.html', context)

def student_portal(request):
    return render(request, 'student_portal.html')

# Signup View
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created! Please log in.")
            return redirect("login")

    return render(request, "signup.html")


# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Admin condition
            if user.username == "AdminXYZ" and user.email == "adminxyz02@gmail.com":
                return redirect("Admin_login")
            else:
                return redirect("user_dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def Admin_signup(request):
    return render(request, "Admin_signup.html")

def Admin_login(request):
    return render(request, "Admin_login.html")

# Admin Dashboard
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")


# User Dashboard
def user_dashboard(request):
    return render(request, "user_dashboard.html")

def login_required_404(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404("Page not found")  # Show 404 instead of login page
        return view_func(request, *args, **kwargs)
    return wrapper

# Subscription
@login_required
def sub_management(request):
    return render(request, "admin_panel/subscription.html", {
        "firebase_config": FIREBASE_CONFIG
    })


# Student Section
@login_required
def admin_admission_management(request):
    return render(request, 'admin_panel/admin_admission_management.html')

@login_required
def admin_students_management(request):
    return render(request, 'admin_panel/admin_students_management.html')

@login_required
@csrf_exempt
def save_students(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            students = data.get('students', [])
            
            # Create Excel file
            filename = f"students_backup_{datetime.now().strftime('%Y%m%d')}.xlsx"
            filepath = os.path.join(settings.MEDIA_ROOT, 'downloads', 'uebs_students', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            workbook = xlsxwriter.Workbook(filepath)
            worksheet = workbook.add_worksheet()
            
            # Write headers
            headers = ['Name', 'Class', 'Section', 'Username', 'Parent', 'Contact', 'Status', 'Email', 'Address', 'DOB', 'Gender']
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)
            
            # Write data
            for row, student in enumerate(students, 1):
                for col, key in enumerate(headers):
                    worksheet.write(row, col, student.get(key, ''))
            
            workbook.close()
            
            return JsonResponse({'status': 'success', 'filename': filename})
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'error': 'Invalid method'}, status=405)

@login_required
def admin_class_management(request):
    return render(request, 'admin_panel/admin_class_management.html')

@login_required
def admin_fee_management(request):
    return render(request, 'admin_panel/admin_fee_management.html')

@login_required
def admin_attendance(request):
    return render(request, 'admin_panel/admin_attendance.html')

@login_required
def admin_grades(request):
    return render(request, 'admin_panel/admin_grades.html')


# Staff Section
@login_required
def admin_teacher_management(request):
    return render(request, 'admin_panel/admin_teacher_management.html')

@login_required
def admin_timetable_generator(request):
    return render(request, 'admin_panel/admin_timetable_generator.html')

@login_required
def admin_salary_management(request):
    return render(request, 'admin_panel/admin_salary_management.html')

@login_required
def admin_staff_attendance(request):
    return render(request, 'admin_panel/admin_staff_attendance.html')


# Finance Section
@login_required
def admin_balancesheet_management(request):
    return render(request, 'admin_panel/admin_balancesheet_management.html')

@login_required
def admin_journal_management(request):
    return render(request, 'admin_panel/admin_journal_management.html')

@login_required
def admin_ledger_management(request):
    return render(request, 'admin_panel/admin_ledger_management.html')

@login_required
def admin_expense_management(request):
    return render(request, 'admin_panel/admin_expense_management.html')

@login_required
def admin_daily_book(request):
    return render(request, 'admin_panel/admin_daily_book.html')

@login_required
def admin_profit_loss(request):
    return render(request, 'admin_panel/profit_loss.html')

@login_required
def admin_income_statement(request):
    return render(request, 'admin_panel/income_statement.html')

@login_required
def admin_trial_balance(request):
    return render(request, 'admin_panel/trial_balance.html')


# Billing Section
@login_required
def admin_invoice(request):
    return render(request, 'admin_panel/admin_invoice.html')

@login_required
def admin_invoice_reports(request):
    return render(request, 'admin_panel/admin_invoice_reports.html')

@login_required
def admin_payments(request):
    return render(request, 'admin_panel/admin_payments.html')

@login_required
def admin_refunds(request):
    return render(request, 'admin_panel/admin_refunds.html')

@login_required
def admin_subscription_payments(request):
    return render(request, 'admin_panel/admin_subscription_payments.html')


# Generation Section
@login_required
def admin_certificate_generator(request):
    return render(request, 'admin_panel/admin_certificate_generator.html')

@login_required
def admin_marks_sheet_generator(request):
    return render(request, 'admin_panel/admin_marks_sheet_generator.html')

@login_required
def admin_student_id_generator(request):
    return render(request, 'admin_panel/admin_student_id_generator.html')

@login_required
def admin_staff_id_generator(request):
    return render(request, 'admin_panel/admin_staff_id_generator.html')


# Academic Section
@login_required
def admin_exam_management(request):
    return render(request, 'admin_panel/admin_exam_management.html')

@login_required
def admin_user_management(request):
    return render(request, 'admin_panel/admin_user_management.html')

@login_required
def admin_inventory_management(request):
    return render(request, 'admin_panel/admin_inventory_management.html')

@login_required
def admin_academic_resources(request):
    return render(request, 'admin_panel/admin_academic_resources.html')

@login_required
def admin_scholarship_tracking(request):
    return render(request, 'admin_panel/admin_scholarship_tracking.html')

@login_required
def admin_bulk_upload(request):
    return render(request, 'admin_panel/admin_bulk_upload.html')


# Reports Section
@login_required
def admin_reports(request):
    return render(request, 'admin_panel/admin_reports.html')

@login_required
def admin_finance_reports(request):
    return render(request, 'admin_panel/admin_finance_reports.html')


# Notices Section
@login_required
def admin_notices_alerts(request):
    return render(request, 'admin_panel/admin_notices_alerts.html')

@login_required
def admin_voice_notices(request):
    return render(request, 'admin_panel/admin_voice_notices.html')

@login_required
def admin_sms_notices(request):
    return render(request, 'admin_panel/admin_sms_notices.html')


# Vehicles Section
@login_required
def admin_vehicles_management(request):
    return render(request, 'admin_panel/admin_vehicles_management.html')

@login_required
def admin_vehicles_track(request):
    return render(request, 'admin_panel/admin_vehicles_track.html')

@login_required
def admin_fuel_maintenance_logs(request):
    return render(request, 'admin_panel/admin_fuel_maintenance_logs.html')


# Contact Section
@login_required
def admin_parent_contact(request):
    return render(request, 'admin_panel/admin_parent_contact.html')

@login_required
def admin_staff_contact(request):
    return render(request, 'admin_panel/admin_staff_contact.html')

@login_required
def admin_community(request):
    return render(request, 'admin_panel/admin_community.html')


# Tools Section
@login_required
def admin_ai_tools(request):
    return render(request, 'admin_panel/admin_ai_tools.html')

@login_required
def admin_smart_calendar(request):
    return render(request, 'admin_panel/admin_smart_calendar.html')

@login_required
def admin_elearning_platform(request):
    return render(request, 'admin_panel/admin_elearning_platform.html')

@login_required
def notes(request):
    return render(request, 'admin_panel/notes.html')


# Help Section
@login_required
def website_management(request):
    return render(request, 'admin_panel/website_management.html')

@login_required
def admin_ai_chat_assistant(request):
    return render(request, 'admin_panel/admin_ai_chat_assistant.html')

@login_required
def admin_help_support(request):
    return render(request, 'admin_panel/admin_help_support.html')

@login_required
def admin_settings(request):
    return render(request, 'admin_panel/admin_settings.html')

@login_required
def logout_view(request):
    return redirect('login')  # Assuming you have a login URL named 'login'


# planing and budget Section
@login_required
def plan(request):
    return render(request, 'admin_panel/planing.html')


# refer and marketing Section
@login_required
def referral(request):
    return render(request, 'admin_panel/refer_program.html')  

@login_required
def marketing(request):
    return render(request, 'admin_panel/marketing.html')  


def search(request):
    return render(request, "admin_panel/search.html")

def blog(request):
    return render(request, "admin_panel/blog.html")

def agent(request):
    return render(request, "admin_panel/ai_agent.html")

def dev(request):
    return render(request, "admin_panel/developer.html")