from flask import Flask, render_template, request, jsonify
import os
from pytubefix import YouTube, Search
from moviepy.editor import AudioFileClip, concatenate_audioclips
from threading import Thread
import shutil

app = Flask(__name__)

UPLOAD_FOLDER = "mashup_files"
TEMP_FOLDER = "temp_downloads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)


def download_videos(singer_name, num_videos):
    search = Search(singer_name)
    video_urls = []
    count = 0

    for result in search.results:
        if count >= num_videos:
            break
        if hasattr(result, "watch_url"):
            video_urls.append(result.watch_url)
            count += 1

    audio_files = []

    for i, url in enumerate(video_urls):
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        if stream:
            file_path = stream.download(
                output_path=TEMP_FOLDER,
                filename=f"audio_{i}.mp4"
            )
            audio_files.append(file_path)

    return audio_files


def process_audio(audio_files, duration):
    clips = []

    for file in audio_files:
        audio = AudioFileClip(file)
        if audio.duration > duration:
            audio = audio.subclip(0, duration)
        clips.append(audio)

    return clips


def merge_audio(clips, output_filename):
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_filename, codec="libmp3lame", logger=None)

    final_clip.close()
    for clip in clips:
        clip.close()


def cleanup():
    if os.path.exists(TEMP_FOLDER):
        shutil.rmtree(TEMP_FOLDER)
        os.makedirs(TEMP_FOLDER)


def create_mashup_async(singer_name, num_videos, duration):
    audio_files = download_videos(singer_name, num_videos)
    clips = process_audio(audio_files, duration)

    output_file = os.path.join(
        UPLOAD_FOLDER,
        f"{singer_name.replace(' ', '_')}_mashup.mp3"
    )

    merge_audio(clips, output_file)
    cleanup()


# ---------- ROUTES ----------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create_mashup", methods=["POST"])
def create_mashup():
    singer = request.form.get("singer_name")
    videos = int(request.form.get("num_videos"))
    duration = int(request.form.get("duration"))

    thread = Thread(
        target=create_mashup_async,
        args=(singer, videos, duration)
    )
    thread.start()

    return jsonify({
        "success": True,
        "message": f"Mashup for {singer} is being created!"
    })


if __name__ == "__main__":
    app.run(debug=True)