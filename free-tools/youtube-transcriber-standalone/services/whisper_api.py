"""
OpenAI Whisper API transcription service
"""
import asyncio
import aiofiles
from pathlib import Path
from typing import List
import time
from openai import AsyncOpenAI
import httpx

from config import settings
from logger import logger, log_timer, get_logger
from models import AudioChunk, TranscriptChunk

# Module logger
log = get_logger("whisper_api")


class WhisperTranscriber:
    """Service for transcribing audio chunks using OpenAI Whisper API"""

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            timeout=httpx.Timeout(settings.openai_timeout, connect=10.0),
            max_retries=settings.openai_max_retries
        )
        self.model = settings.openai_model
        self.semaphore = asyncio.Semaphore(settings.max_concurrent_chunks)

    async def transcribe_chunks(self, chunks: List[AudioChunk]) -> List[TranscriptChunk]:
        """
        Transcribe multiple audio chunks in parallel

        Args:
            chunks: List of AudioChunk objects to transcribe

        Returns:
            List of TranscriptChunk objects with transcribed text
        """
        with log_timer("transcribe_chunks", total_chunks=len(chunks)):
            log.info("Starting parallel transcription",
                    chunk_count=len(chunks),
                    max_concurrent=settings.max_concurrent_chunks)

            # Create tasks for parallel processing
            tasks = [
                self._transcribe_single_chunk(chunk)
                for chunk in chunks
            ]

            # Process chunks in parallel with semaphore limiting concurrency
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results and handle any errors
            transcript_chunks = []
            failed_chunks = []

            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    log.error("Chunk transcription failed",
                             chunk_index=chunks[i].chunk_index,
                             error=str(result))
                    failed_chunks.append(chunks[i])
                else:
                    transcript_chunks.append(result)

            if failed_chunks:
                log.warning("Some chunks failed transcription",
                           failed_count=len(failed_chunks),
                           failed_indices=[c.chunk_index for c in failed_chunks])
                raise RuntimeError(f"Failed to transcribe {len(failed_chunks)} chunks")

            log.info("Transcription completed",
                    successful_chunks=len(transcript_chunks))

            return sorted(transcript_chunks, key=lambda x: x.chunk_index)

    async def _transcribe_single_chunk(self, chunk: AudioChunk) -> TranscriptChunk:
        """
        Transcribe a single audio chunk

        Args:
            chunk: AudioChunk to transcribe

        Returns:
            TranscriptChunk with transcribed text
        """
        async with self.semaphore:
            chunk_start_time = time.time()

            try:
                log.debug("Transcribing chunk",
                         chunk_index=chunk.chunk_index,
                         file_path=chunk.file_path)

                # Read audio file
                async with aiofiles.open(chunk.file_path, 'rb') as audio_file:
                    audio_data = await audio_file.read()

                # Log file size
                file_size_mb = len(audio_data) / (1024 * 1024)
                log.debug("Sending to Whisper API",
                         chunk_index=chunk.chunk_index,
                         file_size_mb=round(file_size_mb, 2))

                # Call Whisper API
                api_start = time.time()

                response = await self.client.audio.transcriptions.create(
                    model=self.model,
                    file=(Path(chunk.file_path).name, audio_data),
                    response_format="verbose_json",
                    language=None,  # Auto-detect
                    temperature=0.0  # Deterministic
                )

                api_duration = time.time() - api_start

                # Extract transcript text
                transcript_text = response.text

                log.info("Chunk transcribed successfully",
                        chunk_index=chunk.chunk_index,
                        api_duration_seconds=round(api_duration, 2),
                        text_length=len(transcript_text),
                        language=getattr(response, 'language', 'unknown'))

                # Create TranscriptChunk
                transcript_chunk = TranscriptChunk(
                    chunk_index=chunk.chunk_index,
                    text=transcript_text,
                    start_time=chunk.start_time,
                    end_time=chunk.end_time
                )

                return transcript_chunk

            except asyncio.TimeoutError:
                log.error("Whisper API timeout",
                         chunk_index=chunk.chunk_index,
                         timeout_seconds=settings.openai_timeout)
                raise TimeoutError(f"Whisper API timeout for chunk {chunk.chunk_index}")

            except Exception as e:
                total_duration = time.time() - chunk_start_time
                log.error("Failed to transcribe chunk",
                         chunk_index=chunk.chunk_index,
                         error=str(e),
                         duration_seconds=round(total_duration, 2),
                         exc_info=True)
                raise RuntimeError(f"Transcription failed for chunk {chunk.chunk_index}: {str(e)}")

    async def test_connection(self) -> bool:
        """
        Test connection to OpenAI API

        Returns:
            True if connection successful
        """
        try:
            models = await self.client.models.list()
            log.info("OpenAI API connection successful",
                    available_models=len(models.data))
            return True
        except Exception as e:
            log.error("OpenAI API connection failed", error=str(e))
            return False

    def estimate_cost(self, audio_duration_seconds: float) -> float:
        """
        Estimate transcription cost based on audio duration

        Args:
            audio_duration_seconds: Total audio duration

        Returns:
            Estimated cost in USD
        """
        # Whisper API pricing: $0.006 per minute
        cost_per_minute = 0.006
        duration_minutes = audio_duration_seconds / 60
        estimated_cost = duration_minutes * cost_per_minute

        log.debug("Cost estimate",
                 duration_minutes=round(duration_minutes, 2),
                 estimated_cost_usd=round(estimated_cost, 4))

        return estimated_cost


# Singleton instance
transcriber = WhisperTranscriber()
