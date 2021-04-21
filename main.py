from flask import Flask, request, jsonify, render_template
import certifi
from threading import Thread, enumerate
import tasks
import random
import string
import sqlite3
from datetime import datetime
import json

conn = sqlite3.connect('pvd.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS downloads (name text, url text, thread text, date text, status text)')
conn.commit()

app = Flask(__name__)
app.debug = True

def random_name():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))



@app.route("/")
def index():
    conn = sqlite3.connect('pvd.db')
    c = conn.cursor()
    c.execute("SELECT * FROM downloads WHERE status != 'Deleted'")
    results = c.fetchall()
    videos = []
    for row in results:
        videos.append({
            "title": row[0],
            "url": row[1],
            "thread": row[2],
            "date": str(row[3]),
            "status": row[4]
        })
    c.close()
    conn.close()
    return render_template("index.html", videos=videos)


@app.route("/download", methods=['POST'])
def download_video():
    conn = sqlite3.connect('pvd.db')
    c = conn.cursor()
    today = datetime.now()
    today = today.strftime("%Y-%m-%d %H:%M:%S")
    # Get JSON body
    req = request.get_json()
    url = req["url"]
    # Get video info
    title = tasks.get_video_info(url)
    # Set random thread name
    name = random_name()
    # name = "test123"
    # Open new thread with random name
    thread = Thread(target=tasks.threaded_download, args=(url,), name=name)
    thread.daemon = True
    # Start the thread and download the video
    thread.start()
    # Insert DB records
    params = (title, url, name, today, "Downloading")
    c.execute('INSERT INTO downloads VALUES (?,?,?,?,?)', params)
    conn.commit()
    c.close()
    conn.close()
    return jsonify({
        'thread_name': str(thread.name),
        'started': True,
        'title': title
    })


@app.route("/download/status/<name>", methods=["GET"])
def check_thread(name):
    conn = sqlite3.connect('pvd.db')
    c = conn.cursor()
    status = "Complete"
    for t in enumerate():
        if t.getName() == name:
            status = "Downloading"
    # Lookup record in DB
    c.execute("SELECT status FROM downloads WHERE thread = ?", [name])
    result = c.fetchone()
    try:
        if result[0] != status:
            # Update DB record
            c.execute("UPDATE downloads SET status = ? WHERE thread = ?", [status, name])
            conn.commit()
    except:
        pass
    c.close()
    conn.close()
    return jsonify({
        "status": status,
        "name": name
    })


@app.route("/delete/<name>", methods=["GET"])
def delete_video(name):
    conn = sqlite3.connect('pvd.db')
    c = conn.cursor()
    c.execute("DELETE FROM downloads WHERE thread = ?", [name])
    conn.commit()
    c.close()
    conn.close()
    return jsonify({
        "thread": name,
        "success": True,
        "description": "Video deleted from DB"
    })

app.run()
