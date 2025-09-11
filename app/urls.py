from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('academics/', views.academics, name='academics'),
    path('admissions/', views.admissions, name='admissions'),
    path('facilities/', views.facilities, name='facilities'),
    path('events/', views.events, name='events'),
    path('e-learning/', views.learning, name='e-learning'),
    path('faculty/', views.faculty, name='faculty'),
    path('contact/', views.contact, name='contact'),
    path('student-portal/', views.student_portal, name='student_portal'),
    path("404/", views.error, name="404"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("user-dashboard/", views.user_dashboard, name="user_dashboard"),
    path('Admin_signup/', views.Admin_signup, name='Admin_signup'),
    path('Admin_login/', views.Admin_login, name='Admin_login'),


    # subscription management
    path('subscription/', views.sub_management, name='subscription'),
    path('search/', views.search, name='search'),
    path('blog/', views.blog, name='blog'),
    path('ai_agent/', views.agent, name='ai_agent'),
    path('developer/', views.dev, name='developer'),


      # Student Section
    path('admin_admission_management/', views.admin_admission_management, name='admin_admission_management'),
    path('admin_students_management/', views.admin_students_management, name='admin_students_management'),
    path('save-students/', views.save_students, name='save_students'),
    path('class-management/', views.admin_class_management, name='admin_class_management'),
    path('fee-management/', views.admin_fee_management, name='admin_fee_management'),
    path('attendance/', views.admin_attendance, name='admin_attendance'),
    path('grades/', views.admin_grades, name='admin_grades'),
    
    # Staff Section
    path('teacher-management/', views.admin_teacher_management, name='admin_teacher_management'),
    path('timetable-generator/', views.admin_timetable_generator, name='admin_timetable_generator'),
    path('salary-management/', views.admin_salary_management, name='admin_salary_management'),
    path('staff-attendance/', views.admin_staff_attendance, name='admin_staff_attendance'),
    
    # Finance Section
    path('balancesheet-management/', views.admin_balancesheet_management, name='admin_balancesheet_management'),
    path('journal-management/', views.admin_journal_management, name='admin_journal_management'),
    path('ledger-management/', views.admin_ledger_management, name='admin_ledger_management'),
    path('daily-book/', views.admin_daily_book, name='admin_daily_book'),
    path('profit-loss/', views.admin_profit_loss, name='admin_profit_loss'),
    path('income-statement/', views.admin_income_statement, name='admin_income_statement'),
    path('expense-management/', views.admin_expense_management, name='admin_expense_management'),
     path('trial-balance/', views.admin_trial_balance, name='admin_trial_balance'),
    
    # Billing Section
    path('invoice/', views.admin_invoice, name='admin_invoice'),
    path('invoice-reports/', views.admin_invoice_reports, name='admin_invoice_reports'),
    path('payments/', views.admin_payments, name='admin_payments'),
    path('refunds/', views.admin_refunds, name='admin_refunds'),
    path('subscription-payments/', views.admin_subscription_payments, name='admin_subscription_payments'),
    
    # Generation Section
    path('certificate-generator/', views.admin_certificate_generator, name='admin_certificate_generator'),
    path('marks-sheet-generator/', views.admin_marks_sheet_generator, name='admin_marks_sheet_generator'),
    path('student-id-generator/', views.admin_student_id_generator, name='admin_student_id_generator'),
    path('staff-id-generator/', views.admin_staff_id_generator, name='admin_staff_id_generator'),
    
    # Academic Section
    path('exam-management/', views.admin_exam_management, name='admin_exam_management'),
    path('inventory-management/', views.admin_inventory_management, name='admin_inventory_management'),
    path('academic-resources/', views.admin_academic_resources, name='admin_academic_resources'),
    path('scholarship-tracking/', views.admin_scholarship_tracking, name='admin_scholarship_tracking'),
    path('bulk-upload/', views.admin_bulk_upload, name='admin_bulk_upload'),
    path('admin-user-management/', views.admin_user_management, name='admin_user_management'),
    
    # Reports Section
    path('reports/', views.admin_reports, name='admin_reports'),
    path('finance-reports/', views.admin_finance_reports, name='admin_finance_reports'),
    
    # Notices Section
    path('notices-alerts/', views.admin_notices_alerts, name='admin_notices_alerts'),
    path('voice-notices/', views.admin_voice_notices, name='admin_voice_notices'),
    path('sms-notices/', views.admin_sms_notices, name='admin_sms_notices'),
    
    # Vehicles Section
    path('vehicles-management/', views.admin_vehicles_management, name='admin_vehicles_management'),
    path('vehicles-track/', views.admin_vehicles_track, name='admin_vehicles_track'),
    path('fuel-maintenance-logs/', views.admin_fuel_maintenance_logs, name='admin_fuel_maintenance_logs'),
    
    # Contact Section
    path('parent-contact/', views.admin_parent_contact, name='admin_parent_contact'),
    path('staff-contact/', views.admin_staff_contact, name='admin_staff_contact'),
    path('community/', views.admin_community, name='admin_community'),
    
    # Tools Section
    path('ai-tools/', views.admin_ai_tools, name='admin_ai_tools'),
      path('notes/', views.notes, name='notes'),
    path('smart-calendar/', views.admin_smart_calendar, name='admin_smart_calendar'),
    path('elearning-platform/', views.admin_elearning_platform, name='admin_elearning_platform'),
    
    # Help Section
    path('website-management/', views.website_management, name='website_management'),
    path('ai-chat-assistant/', views.admin_ai_chat_assistant, name='admin_ai_chat_assistant'),
    path('help-support/', views.admin_help_support, name='admin_help_support'),
    path('settings/', views.admin_settings, name='admin_settings'),
    path('logout/', views.logout_view, name='logout'),

    # budget and plan Section
    path('planing/', views.plan, name='planing'),

     # marketing & referral  Section
 path('refer_program/', views.referral, name='refer_program'),
 path('marketing/', views.marketing, name='marketing'),

]
