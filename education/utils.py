
import openai
from .models import Question
from django.shortcuts import get_object_or_404
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_question_based_on_context(context):
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",  # Assuming you're using a newer model
            prompt=f"Based on the following context, generate an open-ended question:\n\n{context}",
            temperature=0.5,
            max_tokens=100,
        )
        question_text = response['choices'][0]['text'].strip()
        return question_text
    except Exception as e:
        print(f"Error generating question: {e}")
        return None
    
openai.api_key = settings.OPENAI_API_KEY

def assess_student_answer(question_id, student_answer):
    question = get_object_or_404(Question, id=question_id)
    try:
        prompt = f"Given the question: '{question.question_text}' and the answer: '{student_answer}', evaluate the correctness of the answer and provide a numerical score out of 100."
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0.5,
            max_tokens=100,
        )
        evaluation_text = response['choices'][0]['text'].strip()
        # Parse the response to extract the score
        # Assuming the AI's response format is "Evaluation: [text]. Score: [number]."
        score = extract_score(evaluation_text)
        return evaluation_text, score
    except Exception as e:
        print(f"Error assessing answer: {e}")
        return "Error in assessing the answer. Please try again.", 0

def extract_score(evaluation_text):
    # Simple parsing based on expected format
    try:
        score_text = evaluation_text.split("Score: ")[1].split('.')[0]
        score = int(score_text)
        return score
    except (IndexError, ValueError):
        # Default score or error handling
        return 0
    
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

from django.conf import settings
import openai
import logging

# Configure a logger for your application
logger = logging.getLogger(__name__)

openai.api_key = settings.OPENAI_API_KEY

def generate_content_for_topic(topic_name):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"Create a comprehensive educational context for the topic: '{topic_name}'. Include key concepts and an introduction.",
            temperature=0.5,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        generated_content = response.choices[0].text.strip()
        return generated_content
    except Exception as e:
        # Log the error with traceback
        logger.error(f"Error generating content for topic: {topic_name}", exc_info=True)
        return "Error in generating content. Please try again."