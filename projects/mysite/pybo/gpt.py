import os
import django
import openai
import sqlite3

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_response(S):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": S}
        ]
    )
    return response.choices[0].message.content

def new_question_id():
    conn = sqlite3.connect("/root/projects/mysite/db.sqlite3")
    
    cur = conn.cursor()
    cur.execute("SELECT id FROM pybo_question")
    rows = cur.fetchall()

    return len(rows)+1

def get_forms(request, new_content):
    new_question = get_object_or_404(Question, pk=new_question_id())
    form = AnswerForm(request.POST)
    answer = form.save(commit=False)

    return new_question, form, answer, request, new_content

