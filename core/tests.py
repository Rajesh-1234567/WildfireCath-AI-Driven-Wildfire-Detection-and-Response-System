from django.test import TestCase

# Create your tests here.
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

# Example usage as a simple chatbot
def chat():
    print("Welcome to WildFireCatch 💨🔥")
    while True:
        user_input = input("Enter your transcript text (type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        else:
            summary = generate_gemini_content(user_input, prompt)
            print("\nDetailed Notes:")
            print(summary)
            print("\n")

# Run the chat function
if __name__ == "__main__":
    chat()
