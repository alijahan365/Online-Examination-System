import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import django
from decimal import Decimal
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinexam.settings')
django.setup()

from django.utils import timezone
from exam.models import CourseCategory, Course, Subject, Exam, Question, Enrollment
from teacher.models import Teacher
from student.models import Student

def setup_livemcq():
    print("Setting up Live MCQ™ & Premium EdTech environment...")

    # 1. Clean up obsolete dummy courses with 0 questions (e.g. 2, 3, 4, 5)
    for dummy_id in [2, 3, 4, 5]:
        Course.objects.filter(id=dummy_id).delete()
    print("Cleaned up legacy empty dummy courses.")

    # 2. Get existing Instructors
    t1 = Teacher.objects.filter(user__username='prof_mahmud').first()
    t2 = Teacher.objects.filter(user__username='dr_tanvir').first()
    t3 = Teacher.objects.filter(user__username='engr_nusrat').first()
    if not t1:
        t1 = Teacher.objects.first()
    if not t2:
        t2 = t1
    if not t3:
        t3 = t1

    # 3. Categories
    cat_cse, _ = CourseCategory.objects.get_or_create(
        name='CSE Job & Govt Recruitment',
        defaults={'description': 'BUET, BPSC, Bank and IT Officer Job Exam Preparation', 'icon': 'fas fa-briefcase'}
    )
    cat_web, _ = CourseCategory.objects.get_or_create(
        name='Software Engineering & Web',
        defaults={'description': 'Full-Stack Web Development, Django, REST APIs', 'icon': 'fas fa-code'}
    )
    cat_cp, _ = CourseCategory.objects.get_or_create(
        name='Competitive Programming',
        defaults={'description': 'Data Structures, Algorithms, Problem Solving', 'icon': 'fas fa-laptop-code'}
    )
    cat_bcs, _ = CourseCategory.objects.get_or_create(
        name='BCS & Bank ICT Special',
        defaults={'description': 'Preliminary ICT & Computer Science Section Preparation', 'icon': 'fas fa-graduation-cap'}
    )

    now = timezone.now()
    today_live_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
    today_live_end = today_live_start + timedelta(hours=16) # 8:00 AM to 12:00 AM

    # --- COURSE 1: CSE Job & BUET Master Batch (Premium) ---
    c1, _ = Course.objects.get_or_create(
        id=8,
        defaults={
            'course_name': 'CSE Job & Engineering Special Master Batch',
            'category': cat_cse,
            'teacher': t1,
            'price': Decimal('1500.00'),
            'original_price': Decimal('3000.00'),
            'is_free': False,
            'negative_marking': 0.25,
            'batch_title': 'CSE Job Recruiter Batch 2026',
            'start_time': today_live_start,
            'end_time': today_live_end,
            'result_publish_time': today_live_end + timedelta(minutes=15),
            'routine_date': now.date(),
            'routine_syllabus': 'Data Structures (Arrays, Linked Lists, Trees), DBMS (SQL, Normalization, ACID), OOP & OS',
            'description': 'Bangladesh premier model test program for CSE Graduates preparing for BPSC IT Officer, Bank IT, BUET Written & Ministry Exams.',
        }
    )
    c1.course_name = 'CSE Job & Engineering Special Master Batch'
    c1.price = Decimal('1500.00')
    c1.original_price = Decimal('3000.00')
    c1.is_free = False
    c1.negative_marking = 0.25
    c1.batch_title = 'CSE Job Recruiter Batch 2026'
    c1.start_time = today_live_start
    c1.end_time = today_live_end
    c1.result_publish_time = today_live_end + timedelta(minutes=15)
    c1.routine_date = now.date()
    c1.routine_syllabus = 'Data Structures (Arrays, Linked Lists, Trees), DBMS (SQL, Normalization, ACID), OOP & OS'
    c1.description = 'Bangladesh premier model test program for CSE Graduates preparing for BPSC IT Officer, Bank IT, BUET Written & Ministry Exams.'
    c1.save()

    # --- COURSE 2: Full-Stack Web Development with Django (Premium) ---
    c2, _ = Course.objects.get_or_create(
        id=9,
        defaults={
            'course_name': 'Full-Stack Web Engineering Career Track',
            'category': cat_web,
            'teacher': t2,
            'price': Decimal('2000.00'),
            'original_price': Decimal('4000.00'),
            'is_free': False,
            'negative_marking': 0.25,
            'batch_title': 'Web Engineering Career Track 2026',
            'start_time': today_live_start,
            'end_time': today_live_end,
            'result_publish_time': today_live_end + timedelta(minutes=15),
            'routine_date': now.date() + timedelta(days=1),
            'routine_syllabus': 'Python Fundamentals, Django MVT Architecture, ORM Optimization, REST APIs & PostgreSQL',
            'description': 'Master professional web development with Django, PostgreSQL, Cloud Deployment, and realistic interview exams.',
        }
    )
    c2.course_name = 'Full-Stack Web Engineering Career Track'
    c2.price = Decimal('2000.00')
    c2.original_price = Decimal('4000.00')
    c2.is_free = False
    c2.negative_marking = 0.25
    c2.batch_title = 'Web Engineering Career Track 2026'
    c2.start_time = today_live_start
    c2.end_time = today_live_end
    c2.routine_date = now.date() + timedelta(days=1)
    c2.routine_syllabus = 'Python Fundamentals, Django MVT Architecture, ORM Optimization, REST APIs & PostgreSQL'
    c2.save()

    # --- COURSE 3: Competitive Programming & Algorithms (Premium) ---
    c3, _ = Course.objects.get_or_create(
        id=10,
        defaults={
            'course_name': 'Competitive Programming & Problem Solving Pro',
            'category': cat_cp,
            'teacher': t1,
            'price': Decimal('1000.00'),
            'original_price': Decimal('2000.00'),
            'is_free': False,
            'negative_marking': 0.25,
            'batch_title': 'CP Contestants Batch 01',
            'start_time': today_live_start,
            'end_time': today_live_end,
            'routine_date': now.date() + timedelta(days=2),
            'routine_syllabus': 'Time & Space Complexity, Sorting & Searching, Binary Search, Graph BFS/DFS, DP Basics',
            'description': 'Level up your algorithm skills with competitive programming model tests designed by ICPC regionalists.',
        }
    )
    c3.course_name = 'Competitive Programming & Problem Solving Pro'
    c3.price = Decimal('1000.00')
    c3.original_price = Decimal('2000.00')
    c3.is_free = False
    c3.negative_marking = 0.25
    c3.batch_title = 'CP Contestants Batch 01'
    c3.routine_date = now.date() + timedelta(days=2)
    c3.routine_syllabus = 'Time & Space Complexity, Sorting & Searching, Binary Search, Graph BFS/DFS, DP Basics'
    c3.save()

    # --- COURSE 4: BCS & Bank ICT Preliminary Special (Premium) ---
    c4, _ = Course.objects.get_or_create(
        course_name='BCS & Bank ICT Preliminary Special Package',
        defaults={
            'category': cat_bcs,
            'teacher': t3,
            'price': Decimal('800.00'),
            'original_price': Decimal('1600.00'),
            'is_free': False,
            'negative_marking': 0.50,
            'batch_title': '47th BCS & Bank Special 2026',
            'start_time': today_live_start,
            'end_time': today_live_end,
            'routine_date': now.date() + timedelta(days=3),
            'routine_syllabus': 'Computer Fundamentals, Internet & Networking, Cyber Security, Number Systems & Logic Gates',
            'description': 'Complete ICT preparation for 47th BCS Preliminary, Combined Bank Officer & Senior Officer exams.',
        }
    )
    c4.price = Decimal('800.00')
    c4.original_price = Decimal('1600.00')
    c4.is_free = False
    c4.negative_marking = 0.50
    c4.batch_title = '47th BCS & Bank Special 2026'
    c4.routine_date = now.date() + timedelta(days=3)
    c4.routine_syllabus = 'Computer Fundamentals, Internet & Networking, Cyber Security, Number Systems & Logic Gates'
    c4.save()

    # --- COURSE 5: Free Starter & Live Model Test Demo ---
    c5, _ = Course.objects.get_or_create(
        course_name='Free Starter & Live Model Test Demo',
        defaults={
            'category': cat_cse,
            'teacher': t1,
            'price': Decimal('0.00'),
            'original_price': Decimal('0.00'),
            'is_free': True,
            'negative_marking': 0.25,
            'batch_title': 'Free Open Trial 2026',
            'start_time': today_live_start,
            'end_time': today_live_end,
            'routine_date': now.date(),
            'routine_syllabus': 'Open Mock Test covering General CSE, Programming, and AI Webcam Proctoring Verification',
            'description': 'Free open mock test so candidates can test their camera proctoring, timer, and question navigator.',
        }
    )
    c5.is_free = True
    c5.price = Decimal('0.00')
    c5.routine_date = now.date()
    c5.routine_syllabus = 'Open Mock Test covering General CSE, Programming, and AI Webcam Proctoring Verification'
    c5.save()

    # Ensure c5 has at least 5 standard questions
    if c5.questions.count() < 5:
        demo_questions = [
            ("Which data structure operates on LIFO (Last In First Out) principle?", "Queue", "Stack", "Array", "Linked List", "Option2", 2, "A Stack operates on Last-In-First-Out (LIFO) order where the last pushed element is popped first."),
            ("What is the time complexity of searching in a Balanced Binary Search Tree (AVL / Red-Black)?", "O(1)", "O(n)", "O(log n)", "O(n^2)", "Option3", 2, "Balanced BSTs maintain height proportional to log(n), making search O(log n)."),
            ("Which protocol is used for securely transmitting web pages over the internet?", "HTTP", "FTP", "HTTPS", "SMTP", "Option3", 2, "HTTPS (Hypertext Transfer Protocol Secure) encrypts HTTP traffic using TLS/SSL on port 443."),
            ("In Python, which built-in function returns the unique memory identifier of an object?", "type()", "id()", "hash()", "len()", "Option2", 2, "id() returns an integer representing the identity/memory address of an object."),
            ("Which SQL clause is used to filter records based on group aggregate values?", "WHERE", "ORDER BY", "HAVING", "GROUP BY", "Option3", 2, "HAVING filters groups created by GROUP BY, while WHERE filters individual rows before grouping.")
        ]
        for q_text, op1, op2, op3, op4, ans, m, exp in demo_questions:
            Question.objects.create(
                course=c5,
                question=q_text,
                option1=op1,
                option2=op2,
                option3=op3,
                option4=op4,
                answer=ans,
                marks=m,
                explanation=exp
            )

    # Clean up empty courses 6 & 7 if they have only 1-2 demo questions
    for c in [c1, c2, c3, c4, c5]:
        c.question_number = c.questions.count()
        total_m = sum(q.marks for q in c.questions.all())
        c.total_marks = total_m if total_m > 0 else 10
        c.save()

    print("All courses synchronized with realistic Live MCQ pricing, routine and syllabus!")

if __name__ == '__main__':
    setup_livemcq()
