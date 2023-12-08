import os
import openai
import sqlite3
import time

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

    return len(rows)+1, cur

new_cnt, cur = new_question_id()
while True:
    cur.execute("SELECT id FROM pybo_question")
    rows = cur.fetchall()
    if new_cnt == len(rows):
        print("TODO")
        new_cnt += 1
        continue
    else:
        print("FALSE")
        time.sleep(10)
