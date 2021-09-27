import youtube_dl
from flask import jsonify
import moviepy.editor as mp
import os
def threaded_download(url, audioOnly):
	ydl_opts = {
		'nocheckcertificate': True,
		'outtmpl': 'downloads/%(title)s.%(ext)s'
		}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])
	if audioOnly is True:
		download_name = get_video_info(url)
		for file in os.listdir("downloads"):
			if file.startswith(download_name) and file[-4:] != ".mp3":
				search_file = file
		clip_name = "downloads/" + search_file
		final_name = os.path.splitext(clip_name)[0]
		print(clip_name)
		video_clip = mp.VideoFileClip(fr"{clip_name}")
		video_clip.audio.write_audiofile(fr"{final_name}.mp3")
		os.remove(clip_name)


def get_video_info(url):
	ydl_opts = {
		'nocheckcertificate': True
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		info = ydl.extract_info(url, download=False)
		title = info.get('title', None)
	return title
