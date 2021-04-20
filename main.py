from flask import Flask, request, jsonify, render_template
import youtube_dl
import certifi

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=['POST'])
def download():
    req = request.get_json()
    url = req["url"]
    print(url)
    ydl_opts = {'no_check_certificate': True}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return jsonify(url)

app.run()