import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("api_key")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Function to generate completion
def generate_completion(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a roadmap assistant, skilled in explaining which roadmap to follow."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

# Streamlit app
def main():
    st.title("OpenAI RoadMap Recommender Chatbot")
    
    # Get user input
    user_input = st.text_input("Enter your prompt here:")
    
    if st.button("Submit"):
        # Generate completion
        completion = generate_completion(user_input)
        # Display completion
        st.text_area("Response:", value=completion, height=200)

if __name__ == "__main__":
    main()
