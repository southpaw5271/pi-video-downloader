import youtube_dl
from flask import jsonify

def threaded_download(url):
	ydl_opts = {
		'nocheckcertificate': True,
		'outtmpl': 'downloads/%(title)s.%(ext)s'
		}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])


def get_video_info(url):
	ydl_opts = {
		'nocheckcertificate': True
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		info = ydl.extract_info(url, download=False)
		title = info.get('title', None)
	return title
