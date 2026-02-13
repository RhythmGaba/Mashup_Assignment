"""
YouTube Mashup Web Application - IMPROVED VERSION
With better error handling and email debugging
"""

from flask import Flask, render_template, request, jsonify
from pytubefix import YouTube, Search
from moviepy.editor import AudioFileClip, concatenate_audioclips
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import zipfile
import shutil
import traceback
import re
from threading import Thread
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'mashup_files'
TEMP_FOLDER = 'temp_downloads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

# ============================================
# EMAIL CONFIGURATION - UPDATE THESE!
# ============================================
SENDER_EMAIL = "your_email@gmail.com"        # Your Gmail address
SENDER_PASSWORD = "your_app_password"         # Your 16-char App Password from Google

# To get App Password:
# 1. Go to https://myaccount.google.com/apppasswords
# 2. Enable 2-Step Verification first
# 3. Create App Password for "Mail"
# 4. Copy the 16-character password
# 5. Paste it above
# ============================================


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def download_videos(singer_name, num_videos):
    """Download videos from YouTube"""
    try:
        logger.info(f"Searching for {singer_name} videos...")
        search = Search(singer_name)
        video_urls = []
        
        for i, result in enumerate(search.results):
            if i >= num_videos:
                break
            video_urls.append(result.watch_url)
        
        logger.info(f"Found {len(video_urls)} videos")
        audio_files = []
        
        for i, url in enumerate(video_urls):
            try:
                logger.info(f"Downloading {i+1}/{len(video_urls)}: {url}")
                yt = YouTube(url)
                audio_stream = yt.streams.filter(only_audio=True).first()
                
                if audio_stream:
                    output_file = audio_stream.download(
                        output_path=TEMP_FOLDER,
                        filename=f"audio_{i}.mp4"
                    )
                    audio_files.append(output_file)
                    logger.info(f"Downloaded: {output_file}")
                    
            except Exception as e:
                logger.error(f"Error downloading {url}: {str(e)}")
                continue
        
        logger.info(f"Successfully downloaded {len(audio_files)} audio files")
        return audio_files
    
    except Exception as e:
        logger.error(f"Error in download_videos: {str(e)}")
        return []


def process_audio(audio_files, duration):
    """Convert and cut audio files"""
    processed_clips = []
    
    for i, audio_file in enumerate(audio_files):
        try:
            logger.info(f"Processing audio {i+1}/{len(audio_files)}")
            audio_clip = AudioFileClip(audio_file)
            
            if audio_clip.duration > duration:
                cut_clip = audio_clip.subclip(0, duration)
            else:
                cut_clip = audio_clip
            
            processed_clips.append(cut_clip)
            
        except Exception as e:
            logger.error(f"Error processing {audio_file}: {str(e)}")
            continue
    
    logger.info(f"Processed {len(processed_clips)} audio clips")
    return processed_clips


def merge_audio(clips, output_filename):
    """Merge audio clips into single file"""
    try:
        logger.info("Merging audio clips...")
        final_clip = concatenate_audioclips(clips)
        final_clip.write_audiofile(
            output_filename,
            codec='libmp3lame',
            bitrate='192k',
            logger=None
        )
        
        final_clip.close()
        for clip in clips:
            clip.close()
        
        logger.info(f"Mashup created: {output_filename}")
        return True
        
    except Exception as e:
        logger.error(f"Error merging audio: {str(e)}")
        return False


def create_zip(mp3_file, zip_filename):
    """Create a zip file containing the MP3"""
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(mp3_file, os.path.basename(mp3_file))
        logger.info(f"ZIP created: {zip_filename}")
        return True
    except Exception as e:
        logger.error(f"Error creating zip: {str(e)}")
        return False


def send_email(recipient_email, zip_file, singer_name):
    """Send email with zip attachment"""
    try:
        logger.info(f"Preparing to send email to {recipient_email}")
        
        # Check if credentials are configured
        if SENDER_EMAIL == "your_email@gmail.com" or SENDER_PASSWORD == "your_app_password":
            logger.error("Email credentials not configured!")
            logger.error("Please update SENDER_EMAIL and SENDER_PASSWORD in app.py")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = f'🎵 Your Mashup for {singer_name} is Ready!'
        
        # Email body
        body = f"""
Hello!

Your YouTube mashup for "{singer_name}" has been created successfully! 🎉

Please find the attached zip file containing your mashup.

Enjoy your music! 🎵

Best regards,
Mashup Service

---
This is an automated email. Please do not reply.
        """
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach zip file
        logger.info(f"Attaching file: {zip_file}")
        with open(zip_file, 'rb') as attachment:
            part = MIMEBase('application', 'zip')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(zip_file)}'
            )
            msg.attach(part)
        
        # Send email
        logger.info("Connecting to Gmail SMTP server...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            logger.info("Starting TLS...")
            server.starttls()
            
            logger.info("Logging in...")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            
            logger.info("Sending email...")
            server.send_message(msg)
        
        logger.info(f"✅ Email sent successfully to {recipient_email}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        logger.error("❌ SMTP Authentication Error!")
        logger.error("This means your email credentials are incorrect.")
        logger.error("Solutions:")
        logger.error("1. Use App Password, not regular Gmail password")
        logger.error("2. Enable 2-Step Verification in Google Account")
        logger.error("3. Generate App Password at: https://myaccount.google.com/apppasswords")
        logger.error(f"Error details: {e}")
        return False
        
    except Exception as e:
        logger.error(f"❌ Error sending email: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        traceback.print_exc()
        return False


def cleanup_files():
    """Clean up temporary files"""
    try:
        if os.path.exists(TEMP_FOLDER):
            shutil.rmtree(TEMP_FOLDER)
            os.makedirs(TEMP_FOLDER)
        logger.info("Cleanup completed")
    except Exception as e:
        logger.error(f"Error cleaning up: {str(e)}")


def create_mashup_async(singer_name, num_videos, duration, email):
    """Background task to create mashup and send email"""
    try:
        logger.info(f"Starting mashup creation for {singer_name}")
        logger.info(f"Videos: {num_videos}, Duration: {duration}s, Email: {email}")
        
        # Download videos
        audio_files = download_videos(singer_name, num_videos)
        
        if not audio_files:
            logger.error("No audio files downloaded")
            cleanup_files()
            return
        
        # Process audio
        clips = process_audio(audio_files, duration)
        
        if not clips:
            logger.error("No clips processed")
            cleanup_files()
            return
        
        # Merge audio
        safe_name = singer_name.replace(" ", "_").replace("/", "_")
        output_mp3 = os.path.join(UPLOAD_FOLDER, f'{safe_name}_mashup.mp3')
        success = merge_audio(clips, output_mp3)
        
        if not success:
            logger.error("Failed to merge audio")
            cleanup_files()
            return
        
        # Create zip
        output_zip = os.path.join(UPLOAD_FOLDER, f'{safe_name}_mashup.zip')
        create_zip(output_mp3, output_zip)
        
        # Send email
        email_sent = send_email(email, output_zip, singer_name)
        
        if email_sent:
            logger.info(f"✅ Mashup sent successfully to {email}")
        else:
            logger.error(f"❌ Failed to send email to {email}")
            logger.error("Check the error messages above for details")
        
        # Cleanup
        cleanup_files()
        
    except Exception as e:
        logger.error(f"Error in create_mashup_async: {str(e)}")
        traceback.print_exc()
        cleanup_files()


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/create_mashup', methods=['POST'])
def create_mashup():
    """Handle mashup creation request"""
    try:
        # Get form data
        singer_name = request.form.get('singer_name')
        num_videos = request.form.get('num_videos')
        duration = request.form.get('duration')
        email = request.form.get('email')
        
        logger.info(f"Received request: {singer_name}, {num_videos} videos, {duration}s, {email}")
        
        # Validate inputs
        if not all([singer_name, num_videos, duration, email]):
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            })
        
        # Validate email
        if not validate_email(email):
            return jsonify({
                'success': False,
                'message': 'Invalid email address'
            })
        
        # Validate numbers
        try:
            num_videos = int(num_videos)
            duration = int(duration)
            
            if num_videos <= 10:
                return jsonify({
                    'success': False,
                    'message': 'Number of videos must be greater than 10'
                })
            
            if duration <= 20:
                return jsonify({
                    'success': False,
                    'message': 'Duration must be greater than 20 seconds'
                })
                
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Number of videos and duration must be valid numbers'
            })
        
        # Check email configuration
        if SENDER_EMAIL == "your_email@gmail.com":
            return jsonify({
                'success': False,
                'message': 'Email not configured! Please update SENDER_EMAIL and SENDER_PASSWORD in app.py'
            })
        
        # Start background task
        thread = Thread(
            target=create_mashup_async,
            args=(singer_name, num_videos, duration, email)
        )
        thread.start()
        
        return jsonify({
            'success': True,
            'message': f'Your mashup is being created! You will receive an email at {email} shortly. Check your spam folder if you don\'t see it in a few minutes.'
        })
        
    except Exception as e:
        logger.error(f"Error in create_mashup: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("YouTube Mashup Web Application")
    print("="*60)
    print(f"Email configured: {'✅ YES' if SENDER_EMAIL != 'your_email@gmail.com' else '❌ NO'}")
    if SENDER_EMAIL == "your_email@gmail.com":
        print("\n⚠️  WARNING: Email credentials not configured!")
        print("Please update SENDER_EMAIL and SENDER_PASSWORD in app.py")
        print("See EMAIL_SETUP_GUIDE.md for instructions\n")
    print("="*60)
    print("Starting server on http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)