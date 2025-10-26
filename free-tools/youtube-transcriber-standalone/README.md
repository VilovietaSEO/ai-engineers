# YouTube Transcriber - Standalone Tool

A simple, standalone command-line tool for downloading YouTube videos and generating accurate transcripts using OpenAI's Whisper API.

## Features

- **YouTube Audio Download**: Automatically downloads audio from YouTube videos
- **MP3 Extraction**: Converts video to audio format optimized for transcription
- **Whisper Transcription**: Uses OpenAI's state-of-the-art Whisper API for accurate speech-to-text
- **Multiple Output Formats**: Supports TXT, JSON, and SRT subtitle formats
- **Parallel Processing**: Splits long videos into chunks for faster transcription
- **Cost Estimation**: Shows estimated OpenAI API costs before processing
- **Progress Logging**: Detailed logging with progress tracking

## What's Included

This standalone tool contains **only** the core transcription functionality:
- YouTube video download
- Audio extraction to MP3
- Transcript generation via OpenAI Whisper

**Not included**: Blog generation, article formatting, Claude AI integration, or web interface features.

## Requirements

### System Requirements

1. **Python 3.8+**
2. **FFmpeg** (required for audio processing)
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - Windows: [Download from ffmpeg.org](https://ffmpeg.org/download.html)

### API Requirements

- **OpenAI API Key** with access to Whisper API
  - Get your key at: https://platform.openai.com/api-keys
  - Current pricing: $0.006 per minute of audio

## Installation

1. **Clone or download this folder** to your local machine

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your configuration**:
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env and add your OpenAI API key
   nano .env  # or use your preferred editor
   ```

   At minimum, set your OpenAI API key in `.env`:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

4. **Verify FFmpeg installation**:
   ```bash
   ffmpeg -version
   ```

## Usage

### Basic Transcription

Transcribe a YouTube video to a text file:

```bash
python transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

This will:
1. Download the video's audio
2. Split it into chunks
3. Transcribe using Whisper API
4. Save the transcript to `transcripts/VIDEO_ID_transcript.txt`

### Output Formats

**Plain text** (default):
```bash
python transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID" --format txt
```

**JSON with metadata and timestamps**:
```bash
python transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID" --format json
```

**SRT subtitles**:
```bash
python transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID" --format srt
```

### Get Video Info Without Transcribing

Check video details and cost estimate:

```bash
python transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID" --info-only
```

This shows:
- Video title and duration
- Upload date and channel
- Estimated transcription cost
- No charges incurred

### Verbose Logging

Enable detailed debug logging:

```bash
python transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID" --verbose
```

### Full Command Reference

```bash
python transcribe.py [-h] [-f {txt,json,srt}] [--info-only] [-v] url

Arguments:
  url                   YouTube video URL to transcribe

Options:
  -h, --help           Show help message
  -f, --format         Output format: txt, json, or srt (default: txt)
  --info-only          Get video info without transcribing
  -v, --verbose        Enable verbose logging
```

## Examples

**1. Quick transcription**:
```bash
python transcribe.py "https://youtu.be/dQw4w9WgXcQ"
```

**2. Get detailed JSON output**:
```bash
python transcribe.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -f json
```

**3. Generate subtitles**:
```bash
python transcribe.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -f srt
```

**4. Check before transcribing**:
```bash
# First, check the video and cost
python transcribe.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --info-only

# If acceptable, proceed with transcription
python transcribe.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

## Project Structure

```
youtube-transcriber-standalone/
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── .env.example                # Configuration template
├── transcribe.py               # Main CLI script
├── config.py                   # Configuration management
├── logger.py                   # Logging setup
├── models.py                   # Data models
├── services/                   # Core services
│   ├── __init__.py
│   ├── yt_downloader.py        # YouTube download service
│   ├── audio_chunker.py        # Audio splitting service
│   ├── whisper_api.py          # Whisper API integration
│   └── assembler.py            # Transcript assembly service
├── transcripts/                # Output directory (created automatically)
├── audio_chunks/               # Temp chunks (created automatically)
└── temp_downloads/             # Temp downloads (created automatically)
```

## Configuration

All settings can be configured via the `.env` file or environment variables.

### Key Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `OPENAI_API_KEY` | (required) | Your OpenAI API key |
| `CHUNK_SIZE_SECONDS` | 300 | Audio chunk size (5 minutes) |
| `MAX_CONCURRENT_CHUNKS` | 5 | Parallel processing limit |
| `CLEANUP_TEMP_FILES` | true | Auto-delete temporary files |
| `LOG_LEVEL` | INFO | Logging verbosity |

See `.env.example` for all available options.

## How It Works

1. **Download**: Uses yt-dlp to download the video and extract audio
2. **Chunk**: Splits audio into 5-minute chunks with 10-second overlap
3. **Transcribe**: Sends chunks to OpenAI Whisper API in parallel
4. **Assemble**: Combines transcripts, removes overlaps, formats output
5. **Save**: Writes final transcript to the `transcripts/` directory

## Cost Information

OpenAI Whisper API pricing: **$0.006 per minute** of audio

Example costs:
- 10-minute video: ~$0.06
- 30-minute video: ~$0.18
- 1-hour video: ~$0.36
- 2-hour video: ~$0.72

The tool shows cost estimates before processing. Use `--info-only` to check cost without incurring charges.

## Output Files

All transcripts are saved to the `transcripts/` directory with the naming pattern:
```
VIDEO_ID_transcript.{format}
```

**Text format** (`.txt`):
- Clean, readable paragraphs
- No timestamps
- Ready to copy/paste

**JSON format** (`.json`):
- Structured data with metadata
- Individual chunk timestamps
- Full text included
- Easy to parse programmatically

**SRT format** (`.srt`):
- Standard subtitle format
- Timestamps for each segment
- Compatible with video players
- Import into video editing software

## Troubleshooting

### "FFmpeg not found"
Install FFmpeg for your platform (see Requirements section).

### "OpenAI API key not found"
Make sure you've created a `.env` file and set `OPENAI_API_KEY`.

### "Rate limit exceeded"
OpenAI has rate limits. The tool processes chunks in parallel (default: 5 concurrent). Reduce `MAX_CONCURRENT_CHUNKS` in `.env` if needed.

### "Video too long"
Default max duration is 2 hours. Edit `_validate_video()` in `services/yt_downloader.py` to change this.

### "Download failed"
- Check if the video is available and not private
- Some videos may have regional restrictions
- Age-restricted videos may not work

### Cleanup Issues
If temp files aren't being cleaned up, check:
```bash
# In .env
CLEANUP_TEMP_FILES=true
```

Or manually delete:
```bash
rm -rf audio_chunks/* temp_downloads/*
```

## Performance Tips

1. **Faster transcription**: Increase `MAX_CONCURRENT_CHUNKS` (but watch rate limits)
2. **Lower cost**: Use shorter chunks, but this may reduce accuracy
3. **Better accuracy**: Use default chunk size (5 minutes)
4. **Save disk space**: Enable cleanup with `CLEANUP_TEMP_FILES=true`

## Limitations

- Maximum video length: 2 hours (configurable)
- Maximum file size: 500 MB (configurable)
- Requires stable internet connection
- Subject to OpenAI API rate limits
- Private/restricted videos not supported

## License

This tool is provided as-is for personal and educational use.

## Credits

Built with:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text) - Speech recognition
- [pydub](https://github.com/jiaaro/pydub) - Audio processing
- [Loguru](https://github.com/Delgan/loguru) - Logging

---

**Questions or issues?** Check the troubleshooting section above or review the code - it's well-commented and straightforward!
