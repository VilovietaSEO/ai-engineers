"""
Audio chunking service for parallel transcription processing
"""
import os
from pathlib import Path
from typing import List, Tuple
from pydub import AudioSegment
import math

from config import settings
from logger import logger, log_timer, get_logger
from models import AudioChunk

# Module logger
log = get_logger("audio_chunker")


class AudioChunker:
    """Service for splitting audio files into chunks for parallel processing"""

    def __init__(self):
        self.chunks_dir = Path(settings.audio_chunks_dir)
        self.chunks_dir.mkdir(parents=True, exist_ok=True)

        self.chunk_size_ms = settings.chunk_size_seconds * 1000
        self.overlap_ms = settings.chunk_overlap_seconds * 1000

    async def chunk_audio(self, audio_path: str, video_id: str) -> List[AudioChunk]:
        """
        Split audio file into chunks with overlap

        Args:
            audio_path: Path to the audio file
            video_id: Video ID for naming chunks

        Returns:
            List of AudioChunk objects
        """
        with log_timer("chunk_audio", video_id=video_id, audio_path=audio_path):
            try:
                # Load audio file
                log.info("Loading audio file", path=audio_path)
                audio = self._load_audio(audio_path)

                # Calculate chunk parameters
                total_duration_ms = len(audio)
                total_duration_s = total_duration_ms / 1000

                log.info("Audio loaded",
                        duration_seconds=total_duration_s,
                        sample_rate=audio.frame_rate,
                        channels=audio.channels)

                # Split into chunks
                chunks = self._create_chunks(audio, video_id)

                log.info("Chunking completed",
                        video_id=video_id,
                        total_chunks=len(chunks),
                        chunk_size_seconds=settings.chunk_size_seconds,
                        overlap_seconds=settings.chunk_overlap_seconds)

                return chunks

            except Exception as e:
                log.error("Failed to chunk audio",
                         error=str(e),
                         audio_path=audio_path,
                         exc_info=True)
                raise RuntimeError(f"Audio chunking failed: {str(e)}")

    def _load_audio(self, audio_path: str) -> AudioSegment:
        """Load audio file using pydub"""
        try:
            audio = AudioSegment.from_file(audio_path)

            # Convert to mono if needed
            if audio.channels > 1:
                log.debug("Converting to mono")
                audio = audio.set_channels(1)

            # Resample if needed
            if audio.frame_rate != settings.sample_rate:
                log.debug(f"Resampling from {audio.frame_rate} to {settings.sample_rate}")
                audio = audio.set_frame_rate(settings.sample_rate)

            return audio

        except Exception as e:
            log.error("Failed to load audio file", error=str(e))
            raise ValueError(f"Invalid audio file: {str(e)}")

    def _create_chunks(self, audio: AudioSegment, video_id: str) -> List[AudioChunk]:
        """Create overlapping chunks from audio"""
        chunks = []
        chunk_index = 0

        # Calculate step size (chunk size minus overlap)
        step_ms = self.chunk_size_ms - self.overlap_ms

        # Process audio in chunks
        start_ms = 0
        while start_ms < len(audio):
            # Calculate end time for this chunk
            end_ms = min(start_ms + self.chunk_size_ms, len(audio))

            # Extract chunk
            chunk_audio = audio[start_ms:end_ms]

            # Skip if chunk is too small (less than 1 second)
            if len(chunk_audio) < 1000:
                log.warning("Skipping small chunk",
                           chunk_index=chunk_index,
                           duration_ms=len(chunk_audio))
                break

            # Save chunk to file
            chunk_filename = f"{video_id}_chunk_{chunk_index:04d}.{settings.audio_format}"
            chunk_path = self.chunks_dir / chunk_filename

            # Export with consistent parameters
            chunk_audio.export(
                chunk_path,
                format=settings.audio_format,
                parameters=["-q:a", "2"]  # High quality
            )

            # Create AudioChunk object
            chunk = AudioChunk(
                chunk_index=chunk_index,
                file_path=str(chunk_path),
                start_time=start_ms / 1000.0,
                end_time=end_ms / 1000.0,
                duration=(end_ms - start_ms) / 1000.0
            )
            chunks.append(chunk)

            log.debug("Created chunk",
                     chunk_index=chunk_index,
                     start_time=chunk.start_time,
                     end_time=chunk.end_time,
                     duration=chunk.duration,
                     file_size_kb=os.path.getsize(chunk_path) / 1024)

            # Move to next chunk
            start_ms += step_ms
            chunk_index += 1

        return chunks

    def cleanup_chunks(self, chunks: List[AudioChunk]):
        """Clean up chunk files after processing"""
        if not settings.cleanup_temp_files:
            log.debug("Cleanup disabled in settings")
            return

        for chunk in chunks:
            try:
                if os.path.exists(chunk.file_path):
                    os.remove(chunk.file_path)
                    log.debug("Cleaned up chunk", file_path=chunk.file_path)
            except Exception as e:
                log.warning("Failed to cleanup chunk",
                           file_path=chunk.file_path,
                           error=str(e))

    def get_chunk_info(self, audio_duration_seconds: float) -> Tuple[int, float]:
        """
        Calculate chunk information for an audio duration

        Returns:
            Tuple of (number_of_chunks, actual_chunk_duration)
        """
        chunk_size_s = settings.chunk_size_seconds
        overlap_s = settings.chunk_overlap_seconds
        step_s = chunk_size_s - overlap_s

        if audio_duration_seconds <= chunk_size_s:
            return 1, audio_duration_seconds

        num_chunks = math.ceil((audio_duration_seconds - overlap_s) / step_s)

        return num_chunks, chunk_size_s


# Singleton instance
chunker = AudioChunker()
