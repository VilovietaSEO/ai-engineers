"""
Transcript assembly service - combines chunks and formats output
"""
import json
import os
from pathlib import Path
from typing import List, Tuple
from datetime import timedelta
import re

from config import settings
from logger import logger, log_timer, get_logger
from models import TranscriptChunk, TranscriptFormat

# Module logger
log = get_logger("assembler")


class TranscriptAssembler:
    """Service for assembling transcript chunks into final output"""

    def __init__(self):
        self.transcripts_dir = Path(settings.transcripts_dir)
        self.transcripts_dir.mkdir(parents=True, exist_ok=True)

    async def assemble_transcript(
        self,
        chunks: List[TranscriptChunk],
        video_id: str,
        video_title: str,
        output_format: TranscriptFormat
    ) -> Tuple[str, str, int]:
        """
        Assemble transcript chunks into final output

        Args:
            chunks: List of TranscriptChunk objects
            video_id: YouTube video ID
            video_title: Video title for metadata
            output_format: Desired output format

        Returns:
            Tuple of (transcript_text, file_path, word_count)
        """
        with log_timer("assemble_transcript",
                      video_id=video_id,
                      chunk_count=len(chunks),
                      format=output_format.value):

            log.info("Starting transcript assembly",
                    video_id=video_id,
                    total_chunks=len(chunks),
                    format=output_format.value)

            # Sort chunks by index
            sorted_chunks = sorted(chunks, key=lambda x: x.chunk_index)

            # Remove overlapping text between chunks
            cleaned_chunks = self._remove_overlap(sorted_chunks)

            # Merge all text
            full_text = self._merge_chunks(cleaned_chunks)

            # Format based on requested type
            if output_format == TranscriptFormat.JSON:
                formatted_output = self._format_json(cleaned_chunks, video_id, video_title)
            elif output_format == TranscriptFormat.SRT:
                formatted_output = self._format_srt(cleaned_chunks)
            elif output_format == TranscriptFormat.TXT:
                formatted_output = self._format_txt(full_text)
            else:
                raise ValueError(f"Unsupported format: {output_format}")

            # Save to file
            file_path = self._save_transcript(
                formatted_output,
                video_id,
                output_format
            )

            # Calculate word count
            word_count = len(full_text.split())

            log.info("Assembly completed",
                    video_id=video_id,
                    word_count=word_count,
                    output_file=file_path,
                    file_size_kb=os.path.getsize(file_path) / 1024)

            return full_text, file_path, word_count

    def _remove_overlap(self, chunks: List[TranscriptChunk]) -> List[TranscriptChunk]:
        """Remove overlapping text between consecutive chunks"""
        if len(chunks) <= 1:
            return chunks

        cleaned_chunks = []
        overlap_seconds = settings.chunk_overlap_seconds

        for i, chunk in enumerate(chunks):
            if i == len(chunks) - 1:
                # Last chunk - keep as is
                cleaned_chunks.append(chunk)
            else:
                # Trim overlap from end of chunk
                words = chunk.text.split()
                chunk_duration = chunk.end_time - chunk.start_time

                if chunk_duration > overlap_seconds:
                    # Calculate percentage of text to keep
                    keep_ratio = (chunk_duration - overlap_seconds) / chunk_duration
                    words_to_keep = int(len(words) * keep_ratio)

                    # Create new chunk with trimmed text
                    trimmed_text = ' '.join(words[:words_to_keep])

                    cleaned_chunk = TranscriptChunk(
                        chunk_index=chunk.chunk_index,
                        text=trimmed_text,
                        start_time=chunk.start_time,
                        end_time=chunk.end_time - overlap_seconds
                    )
                    cleaned_chunks.append(cleaned_chunk)

                    log.debug("Trimmed chunk overlap",
                             chunk_index=chunk.chunk_index,
                             original_words=len(words),
                             kept_words=words_to_keep)
                else:
                    # Chunk is too small, keep as is
                    cleaned_chunks.append(chunk)

        return cleaned_chunks

    def _merge_chunks(self, chunks: List[TranscriptChunk]) -> str:
        """Merge all chunk texts into a single transcript"""
        texts = []

        for chunk in chunks:
            text = chunk.text.strip()
            if text:
                texts.append(text)

        # Join with space
        full_text = ' '.join(texts)

        # Clean up multiple spaces
        full_text = re.sub(r'\s+', ' ', full_text)

        # Ensure sentences are properly spaced
        full_text = re.sub(r'\.(?=[A-Z])', '. ', full_text)

        return full_text.strip()

    def _format_json(
        self,
        chunks: List[TranscriptChunk],
        video_id: str,
        video_title: str
    ) -> str:
        """Format transcript as JSON with metadata"""
        output = {
            "video_id": video_id,
            "video_title": video_title,
            "chunks": [
                {
                    "index": chunk.chunk_index,
                    "start_time": chunk.start_time,
                    "end_time": chunk.end_time,
                    "text": chunk.text
                }
                for chunk in chunks
            ],
            "full_text": self._merge_chunks(chunks)
        }

        return json.dumps(output, indent=2, ensure_ascii=False)

    def _format_srt(self, chunks: List[TranscriptChunk]) -> str:
        """Format transcript as SRT subtitle file"""
        srt_lines = []

        for i, chunk in enumerate(chunks, 1):
            # Convert times to SRT format
            start_time = self._seconds_to_srt_time(chunk.start_time)
            end_time = self._seconds_to_srt_time(chunk.end_time)

            # Split long text into subtitle-appropriate lines
            text_lines = self._split_text_for_subtitles(chunk.text)

            # Add SRT entry
            srt_lines.append(f"{i}")
            srt_lines.append(f"{start_time} --> {end_time}")
            srt_lines.extend(text_lines)
            srt_lines.append("")  # Empty line between entries

        return '\n'.join(srt_lines)

    def _format_txt(self, text: str) -> str:
        """Format transcript as plain text"""
        # Break into paragraphs at natural points
        paragraphs = []
        sentences = re.split(r'(?<=[.!?])\s+', text)

        current_paragraph = []
        for sentence in sentences:
            current_paragraph.append(sentence)

            # Create new paragraph every ~5 sentences
            if len(current_paragraph) >= 5:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []

        if current_paragraph:
            paragraphs.append(' '.join(current_paragraph))

        return '\n\n'.join(paragraphs)

    def _seconds_to_srt_time(self, seconds: float) -> str:
        """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = td.total_seconds() % 60

        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}".replace('.', ',')

    def _split_text_for_subtitles(self, text: str, max_chars: int = 80) -> List[str]:
        """Split text into subtitle-appropriate lines"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            word_length = len(word) + 1

            if current_length + word_length > max_chars and current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
            else:
                current_line.append(word)
                current_length += word_length

        if current_line:
            lines.append(' '.join(current_line))

        # Limit to 2 lines per subtitle
        if len(lines) > 2:
            mid_point = len(' '.join(lines)) // 2
            line1 = []
            line2 = []
            current_length = 0

            for word in words:
                if current_length < mid_point:
                    line1.append(word)
                else:
                    line2.append(word)
                current_length += len(word) + 1

            lines = [' '.join(line1), ' '.join(line2)]

        return lines

    def _save_transcript(
        self,
        content: str,
        video_id: str,
        format: TranscriptFormat
    ) -> str:
        """Save transcript to file"""
        filename = f"{video_id}_transcript.{format.value}"
        file_path = self.transcripts_dir / filename

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        log.debug("Saved transcript",
                 file_path=str(file_path),
                 size_bytes=len(content.encode('utf-8')))

        return str(file_path)


# Singleton instance
assembler = TranscriptAssembler()
