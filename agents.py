import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def research_agent(topic):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"You are an agricultural research expert. Research this farming topic and provide key facts, common problems and solutions in simple language: {topic}"
        }]
    )
    return response.choices[0].message.content

def content_agent(research, topic):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"You are an agricultural content writer. Based on this research: {research}\n\nCreate simple farming advice content for farmers about: {topic}"
        }]
    )
    return response.choices[0].message.content

def optimization_agent(content, topic):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"You are a content optimizer. Improve this farming content to make it more practical and easy to understand for rural farmers: {content}"
        }]
    )
    return response.choices[0].message.content

def quality_agent(optimized):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"You are a quality checker. Review this farming content and verify it is accurate, safe and helpful for farmers. Give approved version: {optimized}"
        }]
    )
    return response.choices[0].message.content

def distribution_agent(approved, language):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"You are a distribution agent. Take this farming content and format it in {language} language for: 1) WhatsApp message 2) Print pamphlet 3) Radio script. Content: {approved}"
        }]
    )
    return response.choices[0].message.content