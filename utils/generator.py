import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_elimuhub_post(topic):
    prompt = f"""
You are a content creator for Elimuhub Education Consultants, a top tutoring center in Nairobi. 
Write a 100% original, SEO-friendly blog post for the Elimuhub website and social media platforms.

Topic: "{topic}"
Context: You offer home-based tutoring, IGCSE, CBC, KCSE, IB, school placement, homeschooling, and special needs support. 
Mention benefits of Elimuhub's services for parents, learners, or exam candidates in Kenya.

Include:
- A catchy blog title
- A compelling blog body (150-300 words)
- 5 relevant SEO-friendly tags

Output format:
Title: <Blog Title>
Content: <Full Blog HTML-ready content>
Tags: <comma-separated list>
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    output = response['choices'][0]['message']['content']

    try:
        title = output.split("Title:")[1].split("Content:")[0].strip()
        content = output.split("Content:")[1].split("Tags:")[0].strip()
        tags = output.split("Tags:")[1].strip()
    except:
        title, content, tags = "Elimuhub Education Post", output, "Education, Kenya, Tutoring"

    return title, content, tags
