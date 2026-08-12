import os
import gradio as gr
from google import genai


# Get Gemini API key from Render Environment Variables
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")


# Create Gemini client
client = genai.Client(api_key=API_KEY)


# Function for the Study Assistant
def study_assistant(question, level):

    if not question.strip():
        return "Please enter a question or topic."

    prompt = f"""
You are an Interactive Study Assistant designed to help students
understand academic topics clearly.

Student Learning Level:
{level}

Student Question or Topic:
{question}

Instructions:

1. Explain the topic clearly according to the student's learning level.
2. Use simple and understandable language.
3. Give examples wherever useful.
4. Highlight important points.
5. If the topic is difficult, divide it into smaller sections.
6. Use bullet points when appropriate.
7. Help the student understand the concept rather than simply giving
   a very short answer.
8. Keep the response educational and relevant to the question.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"Error generating response: {str(e)}"


# Create Gradio interface
interface = gr.Interface(

    fn=study_assistant,

    inputs=[

        gr.Textbox(
            label="Ask a Question or Enter a Topic",
            placeholder="Example: Explain Machine Learning in simple terms.",
            lines=5
        ),

        gr.Dropdown(
            choices=[
                "Beginner",
                "Intermediate",
                "Advanced"
            ],
            value="Beginner",
            label="Learning Level"
        )

    ],

    outputs=gr.Textbox(
        label="Study Assistant Response",
        lines=18
    ),

    title="Interactive Study Assistant",

    description=(
        "Enter a question or topic, select your learning level, "
        "and get an AI-powered explanation."
    )

)


# Get the port provided by Render
port = int(os.environ.get("PORT", 7860))


# Launch Gradio application
interface.launch(
    server_name="0.0.0.0",
    server_port=port
)
