# 🚀 Quick Start Guide

## Installation (Do this first!)

```bash
# 1. Install dependencies
pip install flask pytubefix moviepy

# 2. Install FFmpeg
# Windows: Download from https://www.gyan.dev/ffmpeg/builds/ and add to PATH
# Mac: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

## Running Command Line Program

```bash
# 1. Rename the file to your roll number
mv mashup.py 1015579.py  # Replace with YOUR roll number

# 2. Run the program
python 1015579.py "Sharry Maan" 20 30 output.mp3

# Format: python <file.py> "<Singer>" <Videos> <Duration> <Output.mp3>
# - Videos must be > 10
# - Duration must be > 20 seconds
```

## Running Web Application

```bash
# 1. Update email credentials in app.py (lines 115-116)
#    - Your Gmail address
#    - Your Gmail App Password (not regular password!)
#    - See README.md for how to get App Password

# 2. Run the app
python app.py

# 3. Open browser
#    Go to: http://localhost:5000

# 4. Fill the form and submit
#    - You'll get the mashup via email!
```

## Testing Examples

```bash
# Test 1: Short and simple
python mashup.py "Arijit Singh" 11 21 test1.mp3

# Test 2: Your actual submission
python 1015579.py "Sharry Maan" 20 30 1015579-output.mp3
```

## Common Errors & Fixes

**"No module named 'pytubefix'"**
→ Run: `pip install pytubefix`

**"FFmpeg not found"**
→ Install FFmpeg (see installation section)

**"No videos downloaded"**
→ Check internet connection or try different singer

**Email not sending (web app)**
→ Update email credentials in app.py with Gmail App Password

## File Structure for Submission

```
Your submission should include:
1. <RollNumber>.py  (e.g., 1015579.py) - Command line program
2. WebApp Link      - Your deployed web application URL
```

## Need Help?

Read the full README.md for:
- Detailed explanations
- Troubleshooting guide
- Deployment instructions
- Code walkthrough

**Good luck! 🎵**