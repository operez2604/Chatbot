import os
import pandas as pd
from flask import Flask, request, jsonify, render_template
from google import genai

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Ruta principal (UI)
@app.route("/")
def home():
    return render_template("index.html")

# Endpoint chatbot
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_question = request.json.get("question").strip()

        if not user_question:
            return jsonify({"error": "No se recibió ninguna pregunta"}), 400

        df = pd.read_excel("data.xlsx")
        context = df.to_string(index=False)

        prompt = f"""
You are a helpful assistant. Answer ONLY using this data:

        {context}

        Question: {user_question}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        answer = response.text
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()