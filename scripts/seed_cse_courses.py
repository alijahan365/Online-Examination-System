"""
Seed Script: Populates realistic CSE Courses, Subjects, Teachers, Exams and MCQs.
"""
import os
import sys
import django
from decimal import Decimal

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinexam.settings')
django.setup()

from django.contrib.auth.models import User, Group
from teacher.models import Teacher
from exam.models import CourseCategory, Course, Subject, Exam, Question

def get_or_create_teacher(username, first_name, last_name, email, mobile, address, salary=55000):
    user, created = User.objects.get_or_create(username=username, defaults={
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
    })
    if created:
        user.set_password('teacher123')
        user.save()
        teacher_group = Group.objects.get_or_create(name='TEACHER')[0]
        teacher_group.user_set.add(user)

    teacher, _ = Teacher.objects.get_or_create(user=user, defaults={
        'mobile': mobile,
        'address': address,
        'salary': salary,
        'status': True
    })
    if not teacher.status:
        teacher.status = True
        teacher.save()
    return teacher

def seed_data():
    print("--- Starting CSE LMS Data Seeding ---")

    # 1. Teachers
    t_tanvir = get_or_create_teacher(
        'dr_tanvir', 'Dr. Tanvir', 'Ahmed', 'tanvir.cse@diu.edu.bd',
        '01711002233', 'Dhanmondi, Dhaka', 65000
    )
    t_mahmud = get_or_create_teacher(
        'prof_mahmud', 'Prof. Mahmudul', 'Hasan', 'mahmud.cse@diu.edu.bd',
        '01819223344', 'Mirpur, Dhaka', 75000
    )
    t_nusrat = get_or_create_teacher(
        'engr_nusrat', 'Engr. Nusrat', 'Jahan', 'nusrat.cse@diu.edu.bd',
        '01911445566', 'Uttara, Dhaka', 55000
    )
    print("Teachers verified.")

    # 2. Categories
    cat_cse, _ = CourseCategory.objects.get_or_create(name="Computer Science & Engineering", defaults={
        'description': 'Core fundamentals of computing, data structures, and computer architecture.',
        'icon': 'fas fa-laptop-code'
    })
    cat_swe, _ = CourseCategory.objects.get_or_create(name="Software Engineering & Web", defaults={
        'description': 'Modern web frameworks, backend systems, APIs, and scalable software architecture.',
        'icon': 'fas fa-code'
    })
    cat_ai, _ = CourseCategory.objects.get_or_create(name="Artificial Intelligence & Data", defaults={
        'description': 'Machine learning, neural networks, predictive modeling, and data science.',
        'icon': 'fas fa-brain'
    })
    cat_cp, _ = CourseCategory.objects.get_or_create(name="Competitive Programming", defaults={
        'description': 'Problem solving, algorithms, C++ STL, and contest programming.',
        'icon': 'fas fa-terminal'
    })
    print("Categories created.")

    # 3. Course 1: CSE Core Fundamentals
    c1, _ = Course.objects.get_or_create(course_name="CSE Core Fundamentals (DSA, DBMS & OOP)", defaults={
        'category': cat_cse,
        'teacher': t_mahmud,
        'description': "Master core computer science topics required for university semester exams, technical job interviews, and software engineering foundations.",
        'price': Decimal('1500.00'),
        'is_free': False,
        'is_active': True,
        'question_number': 30,
        'total_marks': 60
    })

    # Subject 1.1: DSA
    s1_dsa, _ = Subject.objects.get_or_create(course=c1, title="Data Structures & Algorithms (DSA)", defaults={
        'teacher': t_mahmud,
        'description': 'Arrays, Linked Lists, Stacks, Queues, Trees, Graphs, Sorting & Dynamic Programming.',
        'order': 1,
        'is_active': True
    })
    # Exam 1.1.1
    e1_dsa, _ = Exam.objects.get_or_create(subject=s1_dsa, name="Quiz 1: Data Structures Complexity & Arrays", defaults={
        'course': c1,
        'description': 'Evaluation of Big-O notations, array traversal, and pointer operations.',
        'question_number': 5,
        'total_marks': 10,
        'pass_marks': 5,
        'duration_minutes': 15,
        'is_active': True
    })

    dsa_questions = [
        {
            'q': "What is the worst-case time complexity of accessing an element in an array by index?",
            'o1': "O(1)", 'o2': "O(n)", 'o3': "O(log n)", 'o4': "O(n^2)",
            'ans': "Option1", 'exp': "Arrays use contiguous memory locations, allowing direct calculation of memory address in O(1) constant time."
        },
        {
            'q': "Which data structure operates on a Last In First Out (LIFO) order?",
            'o1': "Queue", 'o2': "Stack", 'o3': "Priority Queue", 'o4': "Linked List",
            'ans': "Option2", 'exp': "Stack processes elements on a LIFO basis: the element pushed last is popped first."
        },
        {
            'q': "What is the worst-case time complexity of QuickSort?",
            'o1': "O(n log n)", 'o2': "O(n)", 'o3': "O(n^2)", 'o4': "O(log n)",
            'ans': "Option3", 'exp': "When the pivot chosen is consistently the smallest or largest element, QuickSort degrades to O(n^2)."
        },
        {
            'q': "Which data structure is primarily used in Breadth-First Search (BFS) graph traversal?",
            'o1': "Stack", 'o2': "Queue", 'o3': "Binary Heap", 'o4': "Disjoint Set",
            'ans': "Option2", 'exp': "BFS traverses node level-by-level using a First-In-First-Out Queue."
        },
        {
            'q': "What is the height of a balanced Binary Search Tree containing n nodes?",
            'o1': "O(n)", 'o2': "O(log n)", 'o3': "O(n^2)", 'o4': "O(1)",
            'ans': "Option2", 'exp': "In a balanced BST like AVL or Red-Black Tree, height is bounded by O(log n)."
        }
    ]
    for item in dsa_questions:
        Question.objects.get_or_create(course=c1, question=item['q'], defaults={
            'subject': s1_dsa,
            'exam_paper': e1_dsa,
            'marks': 2,
            'option1': item['o1'],
            'option2': item['o2'],
            'option3': item['o3'],
            'option4': item['o4'],
            'answer': item['ans'],
            'explanation': item['exp']
        })

    # Subject 1.2: DBMS
    s1_dbms, _ = Subject.objects.get_or_create(course=c1, title="Database Management Systems (DBMS)", defaults={
        'teacher': t_nusrat,
        'description': 'Relational data modeling, SQL queries, ER diagrams, normalization (1NF-BCNF), and ACID transactions.',
        'order': 2,
        'is_active': True
    })
    e1_dbms, _ = Exam.objects.get_or_create(subject=s1_dbms, name="Quiz 1: SQL & Normalization Fundamentals", defaults={
        'course': c1,
        'description': 'Tests understanding of Primary/Foreign keys, joins, and normal forms.',
        'question_number': 5,
        'total_marks': 10,
        'pass_marks': 5,
        'duration_minutes': 15,
        'is_active': True
    })

    dbms_questions = [
        {
            'q': "Which SQL statement is used to remove a table along with its structure and data from a database?",
            'o1': "DELETE TABLE", 'o2': "DROP TABLE", 'o3': "REMOVE TABLE", 'o4': "TRUNCATE TABLE",
            'ans': "Option2", 'exp': "DROP TABLE deletes both the definition and all rows from the database permanently."
        },
        {
            'q': "What property guarantees that a database transaction is completed fully or not at all?",
            'o1': "Atomicity", 'o2': "Consistency", 'o3': "Isolation", 'o4': "Durability",
            'ans': "Option1", 'exp': "Atomicity in ACID properties ensures the 'all or nothing' rule for transactions."
        },
        {
            'q': "Which normal form requires eliminating partial dependencies on a composite primary key?",
            'o1': "First Normal Form (1NF)", 'o2': "Second Normal Form (2NF)", 'o3': "Third Normal Form (3NF)", 'o4': "BCNF",
            'ans': "Option2", 'exp': "2NF requires 1NF plus all non-key attributes must be fully functionally dependent on the entire primary key."
        },
        {
            'q': "Which clause in SQL is used to filter group results created by GROUP BY?",
            'o1': "WHERE", 'o2': "ORDER BY", 'o3': "HAVING", 'o4': "FILTER",
            'ans': "Option3", 'exp': "HAVING filters aggregated grouped records, whereas WHERE filters individual rows before grouping."
        },
        {
            'q': "Which type of JOIN returns only matching rows from both joined tables?",
            'o1': "LEFT JOIN", 'o2': "INNER JOIN", 'o3': "FULL OUTER JOIN", 'o4': "CROSS JOIN",
            'ans': "Option2", 'exp': "INNER JOIN matches rows that have common values in both tables based on the join predicate."
        }
    ]
    for item in dbms_questions:
        Question.objects.get_or_create(course=c1, question=item['q'], defaults={
            'subject': s1_dbms,
            'exam_paper': e1_dbms,
            'marks': 2,
            'option1': item['o1'],
            'option2': item['o2'],
            'option3': item['o3'],
            'option4': item['o4'],
            'answer': item['ans'],
            'explanation': item['exp']
        })

    # Subject 1.3: OOP
    s1_oop, _ = Subject.objects.get_or_create(course=c1, title="Object Oriented Programming (OOP)", defaults={
        'teacher': t_tanvir,
        'description': 'Encapsulation, Inheritance, Polymorphism, Abstraction, SOLID principles and design patterns.',
        'order': 3,
        'is_active': True
    })
    e1_oop, _ = Exam.objects.get_or_create(subject=s1_oop, name="Quiz 1: OOP Pillars & Design Principles", defaults={
        'course': c1,
        'description': 'Covers the four pillars of OOP and practical class design.',
        'question_number': 5,
        'total_marks': 10,
        'pass_marks': 5,
        'duration_minutes': 15,
        'is_active': True
    })

    oop_questions = [
        {
            'q': "Which OOP concept is demonstrated by providing the same interface for different underlying forms (datatypes)?",
            'o1': "Encapsulation", 'o2': "Inheritance", 'o3': "Polymorphism", 'o4': "Abstraction",
            'ans': "Option3", 'exp': "Polymorphism allows methods to perform different tasks based on the object invocation (Method Overriding/Overloading)."
        },
        {
            'q': "What is the process of hiding internal details and showing only functionality called?",
            'o1': "Data Hiding", 'o2': "Abstraction", 'o3': "Polymorphism", 'o4': "Modularity",
            'ans': "Option2", 'exp': "Abstraction hides implementation complexities and highlights essential features to the outside world."
        },
        {
            'q': "Which OOP pillar restricts direct access to an object's components by bundling data and methods?",
            'o1': "Encapsulation", 'o2': "Coupling", 'o3': "Cohesion", 'o4': "Inheritance",
            'ans': "Option1", 'exp': "Encapsulation bundles data with methods that manipulate that data, keeping both safe from unauthorized outside access."
        },
        {
            'q': "What does the 'S' stand for in SOLID software design principles?",
            'o1': "Single Responsibility Principle", 'o2': "System Scalability Principle", 'o3': "Structural Inheritance", 'o4': "Stateful Design",
            'ans': "Option1", 'exp': "Single Responsibility Principle asserts that a class should have one, and only one, reason to change."
        },
        {
            'q': "What mechanism allows a child class to provide a specific implementation of a method already provided by its parent?",
            'o1': "Method Overloading", 'o2': "Method Overriding", 'o3': "Shadowing", 'o4': "Duck Typing",
            'ans': "Option2", 'exp': "Method Overriding redefines a parent class method inside a subclass with matching signature."
        }
    ]
    for item in oop_questions:
        Question.objects.get_or_create(course=c1, question=item['q'], defaults={
            'subject': s1_oop,
            'exam_paper': e1_oop,
            'marks': 2,
            'option1': item['o1'],
            'option2': item['o2'],
            'option3': item['o3'],
            'option4': item['o4'],
            'answer': item['ans'],
            'explanation': item['exp']
        })

    # 4. Course 2: Full-Stack Web Development with Django & Python
    c2, _ = Course.objects.get_or_create(course_name="Full-Stack Web Development with Python & Django", defaults={
        'category': cat_swe,
        'teacher': t_tanvir,
        'description': "Build professional web applications from scratch. Covers Django MTV pattern, ORM queries, REST APIs, authentication, and deployment on cloud platforms.",
        'price': Decimal('2000.00'),
        'is_free': False,
        'is_active': True,
        'question_number': 20,
        'total_marks': 40
    })

    s2_django, _ = Subject.objects.get_or_create(course=c2, title="Django Backend Architecture & ORM", defaults={
        'teacher': t_tanvir,
        'description': 'Models, Views, Templates, URL Routing, Forms, QuerySets, and Middleware.',
        'order': 1,
        'is_active': True
    })

    e2_django, _ = Exam.objects.get_or_create(subject=s2_django, name="Midterm Exam: Django Core Architecture", defaults={
        'course': c2,
        'description': 'Covers MTV architecture, migrations, ORM filter queries, and security.',
        'question_number': 5,
        'total_marks': 10,
        'pass_marks': 5,
        'duration_minutes': 20,
        'is_active': True
    })

    django_questions = [
        {
            'q': "In Django's MTV design pattern, what does 'T' stand for?",
            'o1': "Table", 'o2': "Template", 'o3': "Transmission", 'o4': "Testing",
            'ans': "Option2", 'exp': "Django's MTV stands for Model, Template, and View (Template corresponds to the presentation/UI layer)."
        },
        {
            'q': "Which command is used to apply database schema changes in Django?",
            'o1': "python manage.py makemigrations", 'o2': "python manage.py migrate", 'o3': "python manage.py dbsync", 'o4': "python manage.py commit",
            'ans': "Option2", 'exp': "makemigrations creates migration instructions, and migrate actually applies them to the database."
        },
        {
            'q': "How do you protect a POST form against Cross-Site Request Forgery in Django templates?",
            'o1': "{% secure_token %}", 'o2': "{% csrf_token %}", 'o3': "{% auth_token %}", 'o4': "{% verify_session %}",
            'ans': "Option2", 'exp': "{% csrf_token %} generates a secure token that Django verifies upon form submission."
        },
        {
            'q': "Which Django ORM method returns a queryset containing objects that match the specified lookup parameters?",
            'o1': "Model.objects.get()", 'o2': "Model.objects.filter()", 'o3': "Model.objects.find()", 'o4': "Model.objects.match()",
            'ans': "Option2", 'exp': "filter() returns a QuerySet of matching objects, while get() returns exactly one matching instance or raises an exception."
        },
        {
            'q': "Which middleware handles static files efficiently in production deployments like Render without Nginx?",
            'o1': "GunicornMiddleware", 'o2': "WhiteNoiseMiddleware", 'o3': "StaticFileDaemon", 'o4': "CloudinaryProxy",
            'ans': "Option2", 'exp': "WhiteNoise enables WSGI applications to serve their own static files with compression and caching headers."
        }
    ]
    for item in django_questions:
        Question.objects.get_or_create(course=c2, question=item['q'], defaults={
            'subject': s2_django,
            'exam_paper': e2_django,
            'marks': 2,
            'option1': item['o1'],
            'option2': item['o2'],
            'option3': item['o3'],
            'option4': item['o4'],
            'answer': item['ans'],
            'explanation': item['exp']
        })

    # 5. Course 3: Competitive Programming Mastery (FREE STARTER)
    c3, _ = Course.objects.get_or_create(course_name="Competitive Programming & Problem Solving (Starter)", defaults={
        'category': cat_cp,
        'teacher': t_mahmud,
        'description': "Free foundational course on competitive coding. Learn C++ STL vectors, sets, maps, two-pointer techniques, and binary search strategies.",
        'price': Decimal('0.00'),
        'is_free': True,
        'is_active': True,
        'question_number': 15,
        'total_marks': 30
    })

    s3_cp, _ = Subject.objects.get_or_create(course=c3, title="C++ STL & Problem Solving Strategies", defaults={
        'teacher': t_mahmud,
        'description': 'Standard Template Library data structures, time complexity calculation, and binary search patterns.',
        'order': 1,
        'is_active': True
    })

    e3_cp, _ = Exam.objects.get_or_create(subject=s3_cp, name="Starter Contest: STL & Complexity Evaluation", defaults={
        'course': c3,
        'description': 'Speed evaluation on container operations and binary search logic.',
        'question_number': 5,
        'total_marks': 10,
        'pass_marks': 5,
        'duration_minutes': 15,
        'is_active': True
    })

    cp_questions = [
        {
            'q': "What is the average time complexity of searching an element in std::unordered_map in C++?",
            'o1': "O(1)", 'o2': "O(log n)", 'o3': "O(n)", 'o4': "O(n log n)",
            'ans': "Option1", 'exp': "std::unordered_map is implemented using a hash table, providing O(1) average lookup time."
        },
        {
            'q': "What is the underlying data structure of std::set in C++?",
            'o1': "Hash Table", 'o2': "Red-Black Tree", 'o3': "Dynamic Array", 'o4': "Max Heap",
            'ans': "Option2", 'exp': "std::set is typically implemented as a self-balancing Red-Black Tree, maintaining keys in sorted order with O(log n) operations."
        },
        {
            'q': "Which header file provides std::sort() and std::binary_search() in C++?",
            'o1': "<vector>", 'o2': "<algorithm>", 'o3': "<numeric>", 'o4': "<iterator>",
            'ans': "Option2", 'exp': "<algorithm> provides fundamental algorithmic functions including sort, binary_search, lower_bound, and reverse."
        },
        {
            'q': "What is the prerequisite for performing binary search on an array?",
            'o1': "The elements must be unique", 'o2': "The array must be sorted", 'o3': "The size must be even", 'o4': "Elements must be integers",
            'ans': "Option2", 'exp': "Binary search divides the search space in half at each step, which strictly requires sorted elements."
        },
        {
            'q': "What is the value of 1 << 10 in C++?",
            'o1': "20", 'o2': "1024", 'o3': "100", 'o4': "512",
            'ans': "Option2", 'exp': "Bitwise left shift 1 << 10 is equivalent to 2^10 = 1024."
        }
    ]
    for item in cp_questions:
        Question.objects.get_or_create(course=c3, question=item['q'], defaults={
            'subject': s3_cp,
            'exam_paper': e3_cp,
            'marks': 2,
            'option1': item['o1'],
            'option2': item['o2'],
            'option3': item['o3'],
            'option4': item['o4'],
            'answer': item['ans'],
            'explanation': item['exp']
        })

    print("--- CSE LMS Data Seeding Finished Successfully! ---")

if __name__ == '__main__':
    seed_data()
