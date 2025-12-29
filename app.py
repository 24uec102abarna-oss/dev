import pandas as pd
from flask import Flask,render_template,request
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
app=Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_CODE"))

# Create model (FIXED class name)
model = genai.GenerativeModel("gemini-2.5-flash")

# Load CSV file
df = pd.read_csv("qa_data (1).csv")

# Build context text
context_text = ""
for _, row in df.iterrows():
    context_text += f"Q: {row['question']}\nA: {row['answer']}\n\n"

# Function to ask Gemini
def ask_gemini(query):
    prompt = f"""
You are a Q&A assistant.

Context:
{context_text}

Question: {query}
"""
    response = model.generate_content(prompt)
    return response.text.strip()

# # Chat loop
# while True:
#     user_input = input("You: ")

#     if user_input.lower() == "exit":
#         print("Good bye 👋")
#         break

#     answer = ask_gemini(user_input)
#     print("Gemini:", answer)


@app.route("/",methods=["GET","POST"])
def home():
    answer=""
    if request.method=="POST":
        query=request.form["query"]
        answer=ask_gemini(query)
    return render_template("index.html",answer=answer)



if __name__=="__main___":
    app.run()