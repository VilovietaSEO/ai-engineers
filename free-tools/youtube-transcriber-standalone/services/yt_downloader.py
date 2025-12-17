"""
YouTube audio downloader service using yt-dlp
"""
import os
import yt_dlp
from pathlib import Path
from typing import Optional, Tuple
import asyncio

from config import settings
from logger import logger, log_timer, get_logger
from models import VideoInfo

# Module logger
log = get_logger("yt_downloader")


class YtDlpLogger:
    """Adapter to route yt-dlp logs to our logger"""

    def debug(self, msg):
        log.debug(f"yt-dlp: {msg}")

    def info(self, msg):
        log.info(f"yt-dlp: {msg}")

    def warning(self, msg):
        log.warning(f"yt-dlp: {msg}")

    def error(self, msg):
        log.error(f"yt-dlp: {msg}")


class YouTubeDownloader:
    """Service for downloading audio from YouTube videos"""

    def __init__(self):
        self.temp_dir = Path(settings.temp_download_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        # yt-dlp options for best audio quality in English
        self.ydl_opts = {
            'format': 'worstaudio[language=en]/worstaudio[language=en-US]/worstaudio/worst',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': settings.audio_format,
                'preferredquality': '64',  # 64kbps is sufficient for speech
            }],
            'outtmpl': str(self.temp_dir / '%(id)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'socket_timeout': 30,
            'retries': 3,
            'logger': YtDlpLogger(),
            'ffmpeg_location': r'C:\Users\mikem\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin',
        }

    async def download_audio(self, url: str) -> Tuple[str, VideoInfo]:
        """
        Download audio from YouTube URL and extract metadata

        Args:
            url: YouTube video URL

        Returns:
            Tuple of (audio_file_path, video_info)

        Raises:
            ValueError: Invalid URL or video not found
            RuntimeError: Download failed
            TimeoutError: Download timeout exceeded
        """
        with log_timer("download_audio", url=url):
            try:
                # First, extract video info without downloading
                video_info = await self._extract_video_info(url)

                # Validate video constraints
                self._validate_video(video_info)

                # Download audio
                audio_path = await self._download_with_timeout(url, video_info)

                # Verify file was created and has reasonable size
                self._verify_download(audio_path)

                log.info("Download completed",
                        video_id=video_info.video_id,
                        title=video_info.title,
                        duration=video_info.duration,
                        file_size_mb=os.path.getsize(audio_path) / 1024 / 1024)

                return audio_path, video_info

            except yt_dlp.utils.DownloadError as e:
                log.error("yt-dlp download error", error=str(e), url=url)
                if "Video unavailable" in str(e):
                    raise ValueError(f"Video not available: {url}")
                elif "Private video" in str(e):
                    raise ValueError(f"Cannot access private video: {url}")
                else:
                    raise RuntimeError(f"Download failed: {str(e)}")
            except Exception as e:
                log.error("Unexpected download error", error=str(e), url=url, exc_info=True)
                raise

    async def get_video_info(self, url: str) -> VideoInfo:
        """
        Get video info without downloading

        Args:
            url: YouTube video URL

        Returns:
            VideoInfo object with metadata
        """
        return await self._extract_video_info(url)

    async def _extract_video_info(self, url: str) -> VideoInfo:
        """Extract video metadata without downloading"""
        log.debug("Extracting video info", url=url)

        with yt_dlp.YoutubeDL({**self.ydl_opts, 'skip_download': True}) as ydl:
            info = ydl.extract_info(url, download=False)

            return VideoInfo(
                video_id=info['id'],
                title=info['title'],
                duration=int(info.get('duration', 0)),
                uploader=info.get('uploader', 'Unknown'),
                upload_date=info.get('upload_date', None)
            )

    def _validate_video(self, video_info: VideoInfo):
        """Validate video meets our constraints"""
        max_duration = 3600 * 2  # 2 hours

        if video_info.duration > max_duration:
            raise ValueError(
                f"Video too long: {video_info.duration}s exceeds maximum {max_duration}s"
            )

        if video_info.duration < 1:
            raise ValueError("Invalid video duration")

    async def _download_with_timeout(self, url: str, video_info: VideoInfo) -> str:
        """Download with timeout enforcement"""
        log.info("Starting download", video_id=video_info.video_id)

        # Run yt-dlp in thread pool to avoid blocking
        loop = asyncio.get_event_loop()

        def download_sync():
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])
                # Return the expected file path
                return str(self.temp_dir / f"{video_info.video_id}.{settings.audio_format}")

        try:
            audio_path = await asyncio.wait_for(
                loop.run_in_executor(None, download_sync),
                timeout=settings.download_timeout
            )
            return audio_path
        except asyncio.TimeoutError:
            log.error("Download timeout", video_id=video_info.video_id, timeout=settings.download_timeout)
            raise TimeoutError(f"Download exceeded timeout of {settings.download_timeout}s")

    def _verify_download(self, file_path: str):
        """Verify downloaded file exists and is valid"""
        if not os.path.exists(file_path):
            raise RuntimeError("Downloaded file not found")

        file_size_mb = os.path.getsize(file_path) / 1024 / 1024

        if file_size_mb > settings.max_file_size_mb:
            os.remove(file_path)
            raise ValueError(f"File too large: {file_size_mb:.1f}MB exceeds maximum {settings.max_file_size_mb}MB")

        if file_size_mb < 0.1:  # Less than 100KB
            os.remove(file_path)
            raise RuntimeError("Downloaded file is too small, likely corrupted")

    def cleanup_temp_file(self, file_path: str):
        """Clean up temporary download file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                log.debug("Cleaned up temp file", file_path=file_path)
        except Exception as e:
            log.warning("Failed to cleanup temp file", file_path=file_path, error=str(e))


# Singleton instance
downloader = YouTubeDownloader()
