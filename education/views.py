from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.
from django.http import JsonResponse
from .utils import generate_question_based_on_context,  generate_content_for_topic, assess_student_answer
from .models import Topic, Question,StudentResponse

from django.shortcuts import render, redirect
from .forms import TopicForm, ResponseForm

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, LoginForm

def welcome_page(request):
    return render(request, "base.html")

def register_request(request):
    submitted =False
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")  # Redirect to a home page or dashboard
        else: 
            submitted = True
    else:
        form = RegisterForm()
    return render(request, "education/register.html", {"form": form})

def login_request(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("submit_topic")  # Redirect to a home page or dashboard
    else:
        form = LoginForm()
    return render(request, "education/login.html", {"form": form})

@login_required
def submit_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.creator = request.user
            topic.save()
            generated_content = generate_content_for_topic(topic.name)
            question_text = generate_question_based_on_context(generated_content)
            if question_text:  # Check if question_text is not None
                Question.objects.create(topic=topic, context=generated_content, question_text=question_text)
                return redirect('topic_submitted')  # Ensure this URL name is correctly defined in urls.py
            else:
                # Redirect to the error page with a custom message
                return render(request, 'education/error.html', {'error': 'Failed to generate a question. Please try again.'})
    else:
        form = TopicForm()
    return render(request, 'education/submit_topic.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from .models import Question

@login_required
def topic_submitted(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'education/topic_submitted.html', {'question': question})

@login_required    
def submit_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            student_answer = form.cleaned_data['student_answer']
            evaluation, score = assess_student_answer(question.id, student_answer)
            student_response = StudentResponse.objects.create(
                question=question,
                student_answer=student_answer,
                evaluation=evaluation,
                score=score,
            )
            return render(request, 'education/answer_evaluation.html', {'student_response': student_response})
        else:
            return render(request, 'education/topic_submitted.html', {'question': question, 'form': form})
    else:
        return redirect('topic_submitted', question_id=question_id)