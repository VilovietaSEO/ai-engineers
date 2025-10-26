# YouTube Transcriber - Standalone Tool

A simple, standalone command-line tool for downloading YouTube videos and generating accurate transcripts using OpenAI's Whisper API.

## 🎯 What It Does

Downloads any YouTube video and generates professional transcripts in multiple formats:

- **TXT** - Plain text transcript
- **JSON** - Structured data with timestamps
- **SRT** - Subtitle format for video players

Uses OpenAI's state-of-the-art Whisper API for highly accurate speech-to-text conversion.

## ✨ Features

✅ **YouTube Audio Download** - Automatically downloads audio from YouTube videos
✅ **MP3 Extraction** - Converts video to audio optimized for transcription
✅ **Whisper Transcription** - OpenAI's best-in-class speech-to-text
✅ **Multiple Output Formats** - TXT, JSON, and SRT subtitle formats
✅ **Parallel Processing** - Splits long videos into chunks for faster processing
✅ **Cost Estimation** - Shows estimated OpenAI API costs before processing
✅ **Progress Logging** - Detailed logging with real-time progress tracking

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **FFmpeg** (for audio processing)
   ```bash
   # macOS
   brew install ffmpeg

   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   ```
3. **OpenAI API Key** - Get yours at https://platform.openai.com/api-keys

### Installation

```bash
# 1. Navigate to the folder
cd free-tools/youtube-transcriber-standalone

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up configuration
cp .env.example .env
nano .env  # Add your OpenAI API key
```

### Usage

```bash
# Basic usage - transcribe a YouTube video
python transcribe.py https://www.youtube.com/watch?v=VIDEO_ID

# Specify output format
python transcribe.py https://www.youtube.com/watch?v=VIDEO_ID --format json

# Save to specific directory
python transcribe.py https://www.youtube.com/watch?v=VIDEO_ID --output ./my-transcripts/
```

## 💰 Pricing

OpenAI Whisper API costs: **$0.006 per minute** of audio

Examples:
- 10 minute video: ~$0.06
- 30 minute podcast: ~$0.18
- 1 hour interview: ~$0.36
- 2 hour lecture: ~$0.72

The tool shows estimated cost **before** processing.

## 📊 Example Output

### Text Format (TXT)
```
YouTube Video Transcript
Generated: 2025-10-25 19:59:00
Video URL: https://www.youtube.com/watch?v=VIDEO_ID
Duration: 15:32

[00:00:01] Welcome to today's tutorial on machine learning...
[00:00:15] First, let's discuss the fundamentals of neural networks...
[00:01:30] The key advantage of deep learning is...
```

### JSON Format
```json
{
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "title": "Introduction to Machine Learning",
  "duration": "15:32",
  "generated_at": "2025-10-25T19:59:00Z",
  "segments": [
    {
      "timestamp": "00:00:01",
      "text": "Welcome to today's tutorial on machine learning..."
    },
    {
      "timestamp": "00:00:15",
      "text": "First, let's discuss the fundamentals of neural networks..."
    }
  ]
}
```

### SRT Format (Subtitles)
```
1
00:00:01,000 --> 00:00:15,000
Welcome to today's tutorial on machine learning...

2
00:00:15,000 --> 00:01:30,000
First, let's discuss the fundamentals of neural networks...
```

## 🔧 Configuration Options

Edit `.env` to customize:

```bash
# Audio Processing
CHUNK_SIZE_SECONDS=300        # Process in 5-minute chunks
CHUNK_OVERLAP_SECONDS=10      # 10-second overlap between chunks
MAX_FILE_SIZE_MB=500          # Maximum download size
AUDIO_FORMAT=mp3              # Audio format
SAMPLE_RATE=16000             # Audio quality

# Directories
DOWNLOADS_DIR=./downloads     # Where videos are downloaded
TRANSCRIPTS_DIR=./transcripts # Where transcripts are saved

# Whisper API
WHISPER_MODEL=whisper-1       # OpenAI model to use
```

## 💡 Use Cases

### 1. Podcast Transcription
```bash
# Transcribe podcast episode for show notes
python transcribe.py https://www.youtube.com/watch?v=PODCAST_ID --format txt
```

### 2. Interview Documentation
```bash
# Generate searchable interview transcript
python transcribe.py https://www.youtube.com/watch?v=INTERVIEW_ID --format json
```

### 3. Video Subtitles
```bash
# Create subtitle file for video
python transcribe.py https://www.youtube.com/watch?v=VIDEO_ID --format srt
```

### 4. Lecture Notes
```bash
# Transcribe educational content
python transcribe.py https://www.youtube.com/watch?v=LECTURE_ID --output ./lectures/
```

### 5. Content Repurposing
```bash
# Convert video content to text for blog posts
python transcribe.py https://www.youtube.com/watch?v=VIDEO_ID --format txt
```

## 🛠️ Advanced Features

### Batch Processing
```python
# transcribe_batch.py
from transcribe import transcribe_video

videos = [
    "https://www.youtube.com/watch?v=VIDEO_1",
    "https://www.youtube.com/watch?v=VIDEO_2",
    "https://www.youtube.com/watch?v=VIDEO_3"
]

for video_url in videos:
    print(f"Transcribing: {video_url}")
    transcribe_video(video_url, output_format="txt")
```

### Custom Processing
The tool includes modular components:
- `services/yt_downloader.py` - YouTube download logic
- `services/audio_chunker.py` - Audio splitting
- `services/whisper_api.py` - Whisper API integration
- `services/assembler.py` - Transcript assembly

Import and use these in your own scripts.

## 🔒 Security

### API Key Protection

✅ **Safe:**
- `.env` file is in `.gitignore`
- API key never committed to version control
- `.env.example` only shows template

❌ **Never:**
- Commit your `.env` file
- Share your OpenAI API key
- Hardcode API keys in scripts

### Setup Steps
```bash
# 1. Copy template
cp .env.example .env

# 2. Edit and add your key
nano .env

# 3. Verify it's ignored
git status  # .env should NOT appear
```

## 📁 Output Structure

```
youtube-transcriber-standalone/
├── downloads/              # Downloaded audio files
│   └── VIDEO_ID.mp3
├── transcripts/           # Generated transcripts
│   ├── VIDEO_ID.txt
│   ├── VIDEO_ID.json
│   └── VIDEO_ID.srt
└── logs/                  # Processing logs
    └── transcribe.log
```

## 🐛 Troubleshooting

### FFmpeg Not Found
```bash
# Install FFmpeg
brew install ffmpeg  # macOS
sudo apt-get install ffmpeg  # Linux
```

### OpenAI API Error
- Check your API key in `.env`
- Verify you have credits in your OpenAI account
- Ensure you have Whisper API access enabled

### Download Fails
- Check YouTube video is publicly accessible
- Verify video URL is correct
- Some videos may have download restrictions

### Large Files
- Adjust `MAX_FILE_SIZE_MB` in `.env`
- Tool automatically chunks large files
- Consider processing shorter segments

## 📚 Requirements

See `requirements.txt`:
```
openai>=1.0.0
yt-dlp>=2023.0.0
pydub>=0.25.0
python-dotenv>=1.0.0
requests>=2.31.0
```

## 🔗 Links

- **OpenAI Whisper API:** https://platform.openai.com/docs/guides/speech-to-text
- **FFmpeg Download:** https://ffmpeg.org/download.html
- **yt-dlp Documentation:** https://github.com/yt-dlp/yt-dlp

## 📄 License

MIT

---

**Location:** `/free-tools/youtube-transcriber-standalone/`
**Generated with:** [Claude Code](https://claude.com/claude-code)
**Repository:** https://github.com/VilovietaSEO/ai-engineers
