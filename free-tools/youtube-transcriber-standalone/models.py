"""
Data models for YouTube transcription
"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class TranscriptFormat(str, Enum):
    """Output format options"""
    JSON = "json"
    SRT = "srt"
    TXT = "txt"


class VideoInfo(BaseModel):
    """Video metadata from YouTube"""
    video_id: str
    title: str
    duration: int  # seconds
    uploader: str
    upload_date: Optional[str] = None


class AudioChunk(BaseModel):
    """Represents an audio chunk for processing"""
    chunk_index: int = Field(..., description="Chunk number starting from 0")
    file_path: str = Field(..., description="Path to chunk audio file")
    start_time: float = Field(..., description="Start time in seconds")
    end_time: float = Field(..., description="End time in seconds")
    duration: float = Field(..., description="Chunk duration in seconds")


class TranscriptChunk(BaseModel):
    """Transcribed chunk from Whisper API"""
    chunk_index: int = Field(..., description="Chunk number")
    text: str = Field(..., description="Transcribed text")
    start_time: float = Field(..., description="Start time in seconds")
    end_time: float = Field(..., description="End time in seconds")


class TranscriptionResult(BaseModel):
    """Final transcription result"""
    video_id: str
    video_title: str
    video_duration: int
    transcript: str
    format: TranscriptFormat
    word_count: int
    processing_time: float
    file_path: str
    estimated_cost: float
