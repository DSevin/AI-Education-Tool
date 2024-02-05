from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Question, Topic, StudentResponse  # Adjust imports based on your model structure
from .forms import RegisterForm, LoginForm, TopicForm, ResponseForm  # Adjust imports based on your form structure

class EducationAppViewTests(TestCase):
    
    def setUp(self):
        # Create a user for testing login and submit_topic views
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Create a topic for testing topic_submitted and submit_answer views
        self.topic = Topic.objects.create(name='Test Topic', creator=self.user)
        self.question = Question.objects.create(topic=self.topic, context='Test Context', question_text='Test Question?')
    
    def test_welcome_page(self):
        response = self.client.get(reverse('welcome_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_register_request_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'education/register.html')
        self.assertIsInstance(response.context['form'], RegisterForm)

    def test_register_request_post(self):
        form_data = {'username': 'newuser','email': 'newuser@example.com', 'password1': 'testpass123', 'password2': 'testpass123'}
        response = self.client.post(reverse('register'), data=form_data, follow =True)
        self.assertEqual(User.objects.count(), 2)  # Including the user created in setUp
        self.assertRedirects(response, reverse('login'))

    def test_login_request_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'education/login.html')
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_login_request_post(self):
        self.client.post(reverse('register'), {'username': 'testuser', 'password1': '12345', 'password2': '12345'})
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertRedirects(response, reverse('submit_topic'))

    def test_submit_topic_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('submit_topic'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'education/submit_topic.html')
        self.assertIsInstance(response.context['form'], TopicForm)

    def test_topic_submitted_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('topic_submitted', args=[self.question.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'education/topic_submitted.html')
        self.assertEqual(response.context['question'], self.question)

    # Add more tests as needed for submit_answer and other views, including form validation and post requests

