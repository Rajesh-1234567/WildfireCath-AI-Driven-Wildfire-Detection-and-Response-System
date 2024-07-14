from django.shortcuts import render
from core.models import TeamModel

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

# chatbot
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini Pro API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for the GenerativeModel
prompt = """You are the safety advisor specialized in forest fires, wildfires, and disaster management. 
Provide essential tips and information on prevention, safety protocols during emergencies. 
Concise tips within 250 words. Answer questions related to fire safety and disaster management."""

# Function to generate content using Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

def welcome(request):
    teamdetails=TeamModel.objects.all()
    context={
        'teamdetails':teamdetails,
    }
    return render(request,'core/app/welcome.html',context)

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        if user_message:
            response_message = generate_gemini_content(user_message, prompt)
            return JsonResponse({"reply": response_message})
        return JsonResponse({"reply": "I didn't understand that. Could you please rephrase?"})
    return JsonResponse({"error": "Invalid request method."}, status=405)