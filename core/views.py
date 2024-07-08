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
prompt = """You are a professional advisor specializing in wildfire prevention and the health effects caused by wildfires. Provide concise and beneficial information on wildfire prevention strategies, health impacts, and related topics within 250 words"""

# Function to generate content using Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit UI
st.title("WildFireCatch 💨🔥 Ask your disaster-related issues and tips")
text = st.text_area("Enter Your Transcript Text:")

if st.button("Get Detailed Notes"):
    if text:
        summary = generate_gemini_content(text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
    else:
        st.warning("Please enter some text to generate detailed notes.")



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