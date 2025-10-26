"""
Configuration management for YouTube Transcriber
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # API Keys
    openai_api_key: str = Field(..., description="OpenAI API key for Whisper")

    # Audio Processing
    chunk_size_seconds: int = Field(300, description="Size of audio chunks in seconds (5 minutes)")
    chunk_overlap_seconds: int = Field(10, description="Overlap between chunks for context")
    max_file_size_mb: int = Field(500, description="Maximum file size for downloads")
    audio_format: str = Field("mp3", description="Audio format for processing")
    sample_rate: int = Field(16000, description="Sample rate for audio processing")

    # Paths
    audio_chunks_dir: str = Field("audio_chunks", description="Directory for temporary audio chunks")
    transcripts_dir: str = Field("transcripts", description="Directory for output transcripts")
    temp_download_dir: str = Field("temp_downloads", description="Temporary download directory")

    # OpenAI Configuration
    openai_model: str = Field("whisper-1", description="OpenAI model to use")
    openai_max_retries: int = Field(3, description="Max retries for OpenAI API")
    openai_timeout: int = Field(300, description="Timeout for OpenAI API calls in seconds")

    # Processing Configuration
    max_concurrent_chunks: int = Field(5, description="Maximum concurrent chunk processing")
    cleanup_temp_files: bool = Field(True, description="Clean up temporary files after processing")

    # Logging Configuration
    log_level: str = Field("INFO", description="Logging level (DEBUG, INFO, WARNING, ERROR)")
    log_to_file: bool = Field(False, description="Enable file logging")
    log_file_path: str = Field("logs/app.log", description="Log file path")

    # Request Configuration
    download_timeout: int = Field(600, description="YouTube download timeout in seconds")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "allow"


@lru_cache()
def get_settings():
    """Get cached settings instance"""
    return Settings()


# Convenience instance
settings = get_settings()
