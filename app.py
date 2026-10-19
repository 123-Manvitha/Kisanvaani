import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def research_agent(topic):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"You are an agricultural research expert. Research this farming topic and provide key facts, common problems and solutions in simple language: {topic}"
        }]
    )
    return response.choices[0].message.content

def content_agent(research, topic):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"You are an agricultural content writer. Based on this research: {research}\n\nCreate simple farming advice content for farmers about: {topic}"
        }]
    )
    return response.choices[0].message.content

def optimization_agent(content, topic):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"You are a content optimizer. Improve this farming content to make it more practical and easy to understand for rural farmers: {content}"
        }]
    )
    return response.choices[0].message.content

def quality_agent(optimized):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"You are a quality checker. Review this farming content and verify it is accurate, safe and helpful for farmers. Give approved version: {optimized}"
        }]
    )
    return response.choices[0].message.content

def distribution_agent(approved, language):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"You are a distribution agent. Take this farming content and format it in {language} language for: 1) WhatsApp message 2) Print pamphlet 3) Radio script. Content: {approved}"
        }]
    )
    return response.choices[0].message.content

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    topic = data.get("topic", "")
    language = data.get("language", "Telugu")

    try:
        print("Step 1: Research Agent...")
        research = research_agent(topic)
        print("Research done!")

        print("Step 2: Content Agent...")
        content = content_agent(research, topic)
        print("Content done!")

        print("Step 3: Optimization Agent...")
        optimized = optimization_agent(content, topic)
        print("Optimization done!")

        print("Step 4: Quality Agent...")
        approved = quality_agent(optimized)
        print("Quality done!")

        print("Step 5: Distribution Agent...")
        final = distribution_agent(approved, language)
        print("All done!")

        return jsonify({
            "success": True,
            "research": research,
            "content": content,
            "optimized": optimized,
            "approved": approved,
            "final": final
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)