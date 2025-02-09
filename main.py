import streamlit as st
import os
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)


def generate_completion(prompt):
    # Build a detailed prompt instructing the model to return a JSON list.
    detailed_prompt = (
        "You are a roadmap assistant. Based on the user's input, generate a list of roadmap recommendations. "
        "Return your response as a JSON list where each element is an object with the following keys: "
        "'title' (a short title for the roadmap), "
        "'length' (an estimate of the time or steps required), "
        "'description' (a brief overview), and "
        "'what_to_learn' (a list summarizing what to learn). "
        f"User prompt: {prompt}"
        "Please ensure the response is valid JSON. no text or  ```"
    )

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a roadmap assistant."},
            {"role": "user", "content": detailed_prompt}
        ]
    )
    # Return the text content from the response
    return completion.choices[0].message.content


def main():
    st.title("Roadmap Recommender Chatbot")

    # Get user input
    user_input = st.text_input("Enter your prompt here:")

    if st.button("Submit"):
        # Get the response text from the AI model.
        response_text = generate_completion(user_input)

        # Try to parse the response text as JSON.
        try:
            roadmaps = json.loads(response_text)
        except Exception as e:
            st.error("Error parsing JSON output. The response might not be in valid JSON format.")
            st.text_area("Raw response:", value=response_text, height=200)
            return

        st.subheader("Roadmap Recommendations:")
        for idx, roadmap in enumerate(roadmaps):
            st.markdown(f"### {roadmap.get('title', 'No Title')}")
            st.markdown(f"**Length:** {roadmap.get('length', 'N/A')}")
            st.markdown(f"**Description:** {roadmap.get('description', 'N/A')}")

            # Format the what_to_learn field as bullet points if it's a list.
            what_to_learn = roadmap.get('what_to_learn', 'N/A')
            if isinstance(what_to_learn, list):
                bullet_list = "\n".join([f"- {item}" for item in what_to_learn])
                st.markdown(f"**What to Learn:**\n{bullet_list}")
            else:
                st.markdown(f"**What to Learn:** {what_to_learn}")

            # Divider between roadmap items
            if idx != len(roadmaps) - 1:
                st.markdown("---")


if __name__ == "__main__":
    main()
