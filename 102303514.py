#!/usr/bin/env python3
"""
YouTube Mashup Creator
Downloads videos from YouTube, converts to audio, cuts and merges them.

Usage:
python 102303514.py "SingerName" 20 25 output.mp3
"""

import sys
import os
import shutil
import traceback
from pytubefix import YouTube, Search
from moviepy.editor import AudioFileClip, concatenate_audioclips


# --------------------------------------------------
# Validate Arguments
# --------------------------------------------------
def validate_arguments(args):
    if len(args) != 5:
        print("Usage: python <file.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        return False

    try:
        num_videos = int(args[2])
        if num_videos <= 10:
            print("Error: Number of videos must be greater than 10")
            return False
    except ValueError:
        print("Error: Number of videos must be an integer")
        return False

    try:
        duration = int(args[3])
        if duration <= 20:
            print("Error: Duration must be greater than 20 seconds")
            return False
    except ValueError:
        print("Error: Duration must be an integer")
        return False

    if not args[4].endswith(".mp3"):
        print("Error: Output file must be .mp3")
        return False

    return True


# --------------------------------------------------
# Download Videos
# --------------------------------------------------
def download_videos(singer_name, num_videos):
    print("\nSearching YouTube...\n")

    try:
        search = Search(singer_name)
        video_urls = []
        count = 0

        print(f"Fetching top {num_videos} videos...\n")

        for result in search.results:
            if count >= num_videos:
                break

            # ONLY collect real videos
            if hasattr(result, "watch_url"):
                video_urls.append(result.watch_url)
                print(f"[{count+1}/{num_videos}] Found: {result.title[:60]}...")
                count += 1

        if not video_urls:
            print("No valid videos found.")
            return []

        print("\nDownloading audio...\n")

        temp_dir = "temp_downloads"
        os.makedirs(temp_dir, exist_ok=True)

        audio_files = []

        for i, url in enumerate(video_urls):
            try:
                print(f"[{i+1}/{len(video_urls)}] Downloading...")

                yt = YouTube(url)
                audio_stream = yt.streams.filter(only_audio=True).first()

                if audio_stream:
                    output_path = audio_stream.download(
                        output_path=temp_dir,
                        filename=f"audio_{i}.mp4"
                    )
                    audio_files.append(output_path)
                    print("   ✓ Downloaded")
                else:
                    print("   ✗ No audio stream")

            except Exception as e:
                print("   ✗ Download failed:", e)

        return audio_files

    except Exception as e:
        print("Error during search/download:", e)
        traceback.print_exc()
        return []


# --------------------------------------------------
# Convert & Cut Audio
# --------------------------------------------------
def convert_and_cut_audio(audio_files, duration):
    print("\nProcessing audio files...\n")

    clips = []

    for i, file in enumerate(audio_files):
        try:
            print(f"[{i+1}/{len(audio_files)}] Processing...")

            audio = AudioFileClip(file)

            if audio.duration > duration:
                audio = audio.subclip(0, duration)

            clips.append(audio)
            print("   ✓ Done")

        except Exception as e:
            print("   ✗ Error:", e)

    return clips


# --------------------------------------------------
# Merge Audio
# --------------------------------------------------
def merge_audio_clips(clips, output_filename):
    try:
        print("\nMerging clips...\n")

        final_clip = concatenate_audioclips(clips)

        final_clip.write_audiofile(
            output_filename,
            codec="libmp3lame",
            bitrate="192k",
            logger=None
        )

        final_clip.close()
        for clip in clips:
            clip.close()

        print("\n✓ Mashup created successfully!")
        print("Saved as:", output_filename)

        return True

    except Exception as e:
        print("Error merging:", e)
        traceback.print_exc()
        return False


# --------------------------------------------------
# Cleanup
# --------------------------------------------------
def cleanup():
    if os.path.exists("temp_downloads"):
        shutil.rmtree("temp_downloads")
        print("Temporary files cleaned.")


# --------------------------------------------------
# MAIN
# --------------------------------------------------
def main():
    if not validate_arguments(sys.argv):
        sys.exit(1)

    singer_name = sys.argv[1]
    num_videos = int(sys.argv[2])
    duration = int(sys.argv[3])
    output_filename = sys.argv[4]

    print("\n===== YOUTUBE MASHUP CREATOR =====")
    print("Singer:", singer_name)
    print("Videos:", num_videos)
    print("Clip Duration:", duration)
    print("Output:", output_filename)

    audio_files = download_videos(singer_name, num_videos)

    if not audio_files:
        print("\nNo videos downloaded.")
        sys.exit(1)

    clips = convert_and_cut_audio(audio_files, duration)

    if not clips:
        print("\nNo clips processed.")
        cleanup()
        sys.exit(1)

    success = merge_audio_clips(clips, output_filename)

    cleanup()

    if success:
        print("\n✓ COMPLETED SUCCESSFULLY")
    else:
        print("\n✗ FAILED")


if __name__ == "__main__":
    main()
