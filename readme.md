# YouTube Mashup Creator - Complete Guide

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Installation](#installation)
3. [Program 1: Command Line Tool](#program-1-command-line-tool)
4. [Program 2: Web Application](#program-2-web-application)
5. [How It Works](#how-it-works)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

This project creates mashups from YouTube videos by:
1. Downloading N videos of a specific singer from YouTube
2. Converting videos to audio format
3. Cutting the first Y seconds from each audio
4. Merging all audio clips into a single output file

---

## 🔧 Installation

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed:
```bash
python --version
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install flask pytubefix moviepy
```

### Step 3: Install FFmpeg (Required for audio processing)

**Windows:**
1. Download from: https://www.gyan.dev/ffmpeg/builds/
2. Extract and add to PATH
3. Verify: `ffmpeg -version`

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

---

## 💻 Program 1: Command Line Tool

### File Structure
```
mashup.py          # Main program file (rename to <RollNumber>.py)
requirements.txt   # Dependencies
```

### Usage

**Basic Command:**
```bash
python mashup.py "<SingerName>" <NumberOfVideos> <AudioDuration> <OutputFileName>
```

**Example:**
```bash
python mashup.py "Sharry Maan" 20 30 output.mp3
```

### Parameters Explained

| Parameter | Description | Constraints |
|-----------|-------------|-------------|
| SingerName | Name of the singer/artist | Use quotes for names with spaces |
| NumberOfVideos | Number of videos to download | Must be > 10 |
| AudioDuration | Seconds to cut from each video | Must be > 20 |
| OutputFileName | Name of the final MP3 file | Must end with .mp3 |

### Example Commands

```bash
# Example 1: Arijit Singh, 15 videos, 25 seconds each
python mashup.py "Arijit Singh" 15 25 arijit_mashup.mp3

# Example 2: Ed Sheeran, 20 videos, 30 seconds each
python mashup.py "Ed Sheeran" 20 30 ed_sheeran.mp3

# Example 3: Taylor Swift, 12 videos, 40 seconds each
python mashup.py "Taylor Swift" 12 40 taylor_output.mp3
```

### Error Handling

The program validates:
- ✅ Correct number of arguments (4 required)
- ✅ Number of videos > 10
- ✅ Audio duration > 20 seconds
- ✅ Output file has .mp3 extension
- ✅ Network connectivity issues
- ✅ Download failures
- ✅ Audio processing errors

### Step-by-Step Process

When you run the program, it will:

1. **Validate Arguments**
   - Check if all parameters are provided
   - Verify number constraints
   - Validate file extension

2. **Search YouTube**
   - Search for videos of the specified singer
   - Display found video titles

3. **Download Videos**
   - Download audio streams from YouTube
   - Show progress for each download
   - Handle download errors gracefully

4. **Process Audio**
   - Convert videos to audio format
   - Cut first Y seconds from each audio
   - Display processing status

5. **Merge Audio**
   - Combine all audio clips
   - Create final MP3 file
   - Display success message

6. **Cleanup**
   - Remove temporary files
   - Free up disk space

---

## 🌐 Program 2: Web Application

### File Structure
```
app.py                  # Flask application
templates/
  └── index.html       # Web interface
requirements.txt       # Dependencies
```

### Setup Email Configuration

**IMPORTANT:** Before running, update email settings in `app.py`:

```python
# Line 115-116 in app.py
sender_email = "your_email@gmail.com"      # Your Gmail address
sender_password = "your_app_password"       # Your Gmail App Password
```

### Getting Gmail App Password

1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Go to App Passwords
4. Generate password for "Mail"
5. Copy the 16-character password
6. Use this in `app.py`

### Running the Web Application

```bash
python app.py
```

The server will start at: **http://localhost:5000**

### Using the Web Interface

1. **Open Browser**
   - Navigate to `http://localhost:5000`

2. **Fill Form**
   - Singer Name: e.g., "Sharry Maan"
   - Number of Videos: e.g., 20 (must be > 10)
   - Duration: e.g., 30 (must be > 20)
   - Email: Your email address

3. **Submit**
   - Click "Create Mashup"
   - Wait for confirmation message

4. **Receive Email**
   - Check your email inbox
   - Download the ZIP file
   - Extract to get your mashup MP3

### Web App Features

- ✨ Beautiful, responsive UI
- 🎨 Real-time form validation
- 📧 Automatic email delivery
- 📦 ZIP file packaging
- 🔄 Background processing (non-blocking)
- 🛡️ Error handling and user feedback

---

## 🔍 How It Works

### Technology Stack

1. **pytubefix** - YouTube video downloading
   - Searches for videos by singer name
   - Downloads audio streams
   - Handles YouTube's API changes

2. **moviepy** - Audio processing
   - Converts video to audio
   - Cuts audio to specified duration
   - Merges multiple audio files
   - Exports to MP3 format

3. **Flask** (Web App) - Web framework
   - Handles HTTP requests
   - Renders HTML templates
   - Manages form submissions

4. **smtplib** (Web App) - Email delivery
   - Connects to Gmail SMTP
   - Sends emails with attachments
   - Handles ZIP file delivery

### Workflow Diagram

```
User Input
    ↓
Search YouTube → Find N videos
    ↓
Download Videos → Get audio streams
    ↓
Extract Audio → Convert to audio format
    ↓
Cut Audio → First Y seconds
    ↓
Merge Audio → Combine all clips
    ↓
Export MP3 → Save final file
    ↓
(Web App) Create ZIP → Package the file
    ↓
(Web App) Send Email → Deliver to user
```

### Code Structure Explained

**mashup.py**
```python
validate_arguments()     # Check command line inputs
download_videos()        # Download from YouTube
convert_and_cut_audio()  # Process audio files
merge_audio_clips()      # Combine into one file
cleanup_temp_files()     # Remove temporary files
```

**app.py**
```python
validate_email()         # Check email format
download_videos()        # YouTube download
process_audio()          # Audio processing
merge_audio()            # Audio merging
create_zip()            # Create ZIP file
send_email()            # Email delivery
create_mashup_async()   # Background task
```

---

## 🐛 Troubleshooting

### Common Issues

**1. "Module not found" error**
```bash
# Solution: Install missing package
pip install pytubefix moviepy flask
```

**2. "FFmpeg not found" error**
```bash
# Solution: Install FFmpeg (see installation section above)
# Verify installation:
ffmpeg -version
```

**3. "No videos downloaded"**
```bash
# Possible causes:
- Network connection issues
- YouTube blocking (try VPN)
- Invalid singer name
- YouTube API changes

# Solution: Try different singer name or check internet
```

**4. Email not sending**
```bash
# Check:
- Gmail App Password is correct
- 2-Step Verification is enabled
- Email and password in app.py are correct
- Internet connection is stable
```

**5. "Permission denied" on Linux/Mac**
```bash
# Solution: Make file executable
chmod +x mashup.py
```

### Debug Mode

To see detailed error messages:

**Command Line:**
```python
# Add at the top of mashup.py
import traceback

# In except blocks, add:
traceback.print_exc()
```

**Web App:**
```python
# app.py already has debug=True
# Check console for error messages
```

---

## 📝 Assignment Submission

### For Your Submission

1. **Rename the command line file**
   ```bash
   # Rename mashup.py to your roll number
   mv mashup.py 1015579.py  # Replace with YOUR roll number
   ```

2. **Test the command line program**
   ```bash
   python 1015579.py "Sharry Maan" 20 30 1015579-output.mp3
   ```

3. **Deploy web app** (Choose one):
   - **Render.com** (Free, recommended)
   - **PythonAnywhere** (Free tier available)
   - **Heroku** (Free tier)
   - **Railway** (Free tier)

4. **Submit**
   - Python file: `<RollNumber>.py`
   - WebApp link: Your deployed URL

---

## 🚀 Deployment Guide (Web App)

### Option 1: Render.com (Recommended)

1. Create account on Render.com
2. Create new Web Service
3. Connect GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python app.py`
6. Deploy!

### Option 2: Local Network Access

If you just want to test locally:
```python
# Change in app.py:
app.run(debug=True, host='0.0.0.0', port=5000)

# Access from other devices on same network:
# http://YOUR_LOCAL_IP:5000
```

---

## 📊 Expected Output

### Command Line
```
============================================================
YOUTUBE MASHUP CREATOR
============================================================
Singer: Sharry Maan
Videos to download: 20
Audio duration: 30 seconds
Output file: output.mp3

============================================================
Searching for 'Sharry Maan' videos on YouTube...
============================================================

Fetching top 20 videos...

  [1/20] Found: Sharry Maan - 3 Peg (Official Video)...
  [2/20] Found: Sharry Maan | Hostel | Full Official Video...
  ...

✓ Successfully downloaded 20 audio files

============================================================
Processing audio files (cutting to 30 seconds)...
============================================================

✓ Successfully processed 20 audio clips

============================================================
Merging audio clips...
============================================================

✓ Successfully created mashup!
  Output file: output.mp3
  Total duration: 600.0 seconds

✓ MASHUP COMPLETED SUCCESSFULLY!
```

### Web Interface
User fills form → Receives success message → Gets email with ZIP file

---

## 💡 Tips

1. **Choose popular singers** for better results
2. **Start with smaller numbers** for testing (e.g., 11 videos)
3. **Check internet connection** before running
4. **Use quotes** for singer names with spaces
5. **Verify FFmpeg** is installed before starting

---
