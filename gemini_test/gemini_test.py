import google.generativeai as genai
import os

# Using the key provided by the user
genai.configure(api_key="AIzaSyD-UnYiOPO85QKA8NnOecv68VOZFvSOM2s")

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hello! I am testing the bridge. Are you working?")
    print(f"Gemini response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
