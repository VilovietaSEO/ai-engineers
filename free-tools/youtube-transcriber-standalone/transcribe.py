#!/usr/bin/env python3
"""
YouTube Video Transcriber - Standalone CLI Tool

Downloads YouTube videos, extracts audio, and generates transcripts using OpenAI Whisper API.
"""
import asyncio
import argparse
import sys
import time
from pathlib import Path

from config import settings
from logger import logger, get_logger
from models import TranscriptFormat, TranscriptionResult
from services import downloader, chunker, transcriber, assembler

# Module logger
log = get_logger("main")


async def transcribe_youtube_video(url: str, output_format: TranscriptFormat = TranscriptFormat.TXT) -> TranscriptionResult:
    """
    Main function to transcribe a YouTube video

    Args:
        url: YouTube video URL
        output_format: Output format (txt, json, srt)

    Returns:
        TranscriptionResult with all details
    """
    start_time = time.time()
    audio_path = None
    chunks = []

    try:
        log.info("=" * 60)
        log.info("Starting YouTube transcription")
        log.info(f"URL: {url}")
        log.info(f"Output format: {output_format.value}")
        log.info("=" * 60)

        # Step 1: Download audio
        log.info("Step 1/4: Downloading audio from YouTube...")
        audio_path, video_info = await downloader.download_audio(url)

        # Estimate cost
        estimated_cost = transcriber.estimate_cost(video_info.duration)
        log.info(f"Video: {video_info.title}")
        log.info(f"Duration: {video_info.duration // 60}m {video_info.duration % 60}s")
        log.info(f"Estimated cost: ${estimated_cost:.4f}")

        # Step 2: Chunk audio
        log.info("Step 2/4: Splitting audio into chunks...")
        chunks = await chunker.chunk_audio(audio_path, video_info.video_id)
        log.info(f"Created {len(chunks)} audio chunks")

        # Step 3: Transcribe chunks
        log.info("Step 3/4: Transcribing audio chunks (this may take a while)...")
        transcript_chunks = await transcriber.transcribe_chunks(chunks)
        log.info(f"Successfully transcribed {len(transcript_chunks)} chunks")

        # Step 4: Assemble transcript
        log.info("Step 4/4: Assembling final transcript...")
        full_text, file_path, word_count = await assembler.assemble_transcript(
            transcript_chunks,
            video_info.video_id,
            video_info.title,
            output_format
        )

        processing_time = time.time() - start_time

        # Create result
        result = TranscriptionResult(
            video_id=video_info.video_id,
            video_title=video_info.title,
            video_duration=video_info.duration,
            transcript=full_text,
            format=output_format,
            word_count=word_count,
            processing_time=processing_time,
            file_path=file_path,
            estimated_cost=estimated_cost
        )

        log.info("=" * 60)
        log.info("Transcription completed successfully!")
        log.info(f"Video: {result.video_title}")
        log.info(f"Word count: {result.word_count:,}")
        log.info(f"Processing time: {result.processing_time:.1f}s")
        log.info(f"Output file: {result.file_path}")
        log.info("=" * 60)

        return result

    except Exception as e:
        log.error(f"Transcription failed: {str(e)}", exc_info=True)
        raise

    finally:
        # Cleanup temporary files
        if settings.cleanup_temp_files:
            log.info("Cleaning up temporary files...")
            if audio_path:
                downloader.cleanup_temp_file(audio_path)
            if chunks:
                chunker.cleanup_chunks(chunks)


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Transcribe YouTube videos using OpenAI Whisper API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic transcription to text file
  python transcribe.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

  # Output as JSON with metadata
  python transcribe.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format json

  # Output as SRT subtitles
  python transcribe.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format srt

  # Get video info without transcribing
  python transcribe.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --info-only

Requirements:
  - OpenAI API key set in .env file or OPENAI_API_KEY environment variable
  - FFmpeg installed on your system (for audio processing)
        """
    )

    parser.add_argument(
        "url",
        help="YouTube video URL to transcribe"
    )

    parser.add_argument(
        "-f", "--format",
        choices=["txt", "json", "srt"],
        default="txt",
        help="Output format (default: txt)"
    )

    parser.add_argument(
        "--info-only",
        action="store_true",
        help="Only fetch video information without transcribing"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Set log level
    if args.verbose:
        import os
        os.environ["LOG_LEVEL"] = "DEBUG"

    try:
        # Info-only mode
        if args.info_only:
            async def get_info():
                video_info = await downloader.get_video_info(args.url)
                cost = transcriber.estimate_cost(video_info.duration)

                print("\n" + "=" * 60)
                print("Video Information")
                print("=" * 60)
                print(f"Title: {video_info.title}")
                print(f"Video ID: {video_info.video_id}")
                print(f"Duration: {video_info.duration // 60}m {video_info.duration % 60}s")
                print(f"Uploader: {video_info.uploader}")
                if video_info.upload_date:
                    print(f"Upload date: {video_info.upload_date}")
                print(f"Estimated transcription cost: ${cost:.4f}")
                print("=" * 60 + "\n")

            asyncio.run(get_info())
            return

        # Full transcription
        output_format = TranscriptFormat(args.format)
        result = asyncio.run(transcribe_youtube_video(args.url, output_format))

        # Print summary
        print("\n" + "=" * 60)
        print("TRANSCRIPTION COMPLETE")
        print("=" * 60)
        print(f"Video: {result.video_title}")
        print(f"Video ID: {result.video_id}")
        print(f"Duration: {result.video_duration // 60}m {result.video_duration % 60}s")
        print(f"Words: {result.word_count:,}")
        print(f"Format: {result.format.value}")
        print(f"Processing time: {result.processing_time:.1f}s")
        print(f"Estimated cost: ${result.estimated_cost:.4f}")
        print(f"\nOutput saved to: {result.file_path}")
        print("=" * 60 + "\n")

    except KeyboardInterrupt:
        log.warning("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        log.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
