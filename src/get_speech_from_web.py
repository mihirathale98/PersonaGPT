import requests
import os
# import youtube_dl
import yt_dlp as youtube_dl
import tempfile
from src.brave_search import brave_search
import ffmpeg
import json
import subprocess

class VoiceSearch:
    def __init__(self):
        pass

    def get_speech(self, name):
        query = f"{name} Audio Sample Interview Video YouTube"
        wav_file = self.get_speech_from_youtube(query)
        return wav_file

    def web_search(self, query):
        response = brave_search(query)
        return response

    def get_speech_from_youtube(self, query):
        search_results = self.web_search(query)
        if search_results is None:
            return None
        for res in search_results:
            if '''www.youtube.com/watch?v=''' in res['url']:
                return self.get_audio_from_youtube(res['url'])

    def get_audio_from_youtube(self, video_url):
        temp_video = 'temp_video.mp4'
        output_file = 'output.wav'
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': temp_video,
        }
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        # Get video duration using ffprobe
        probe = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", temp_video], capture_output=True, text=True)
        probe_data = json.loads(probe.stdout)
        duration = float(probe_data['format']['duration'])
        
        # Determine the shorter of 30 seconds or the video duration
        clip_duration = min(30, duration)
        
        # Use ffmpeg to clip and convert to WAV
        subprocess.run([
            "ffmpeg",
            "-i", temp_video,
            "-t", str(clip_duration),
            "-acodec", "pcm_s16le",  # 16-bit PCM codec for WAV
            "-ar", "44100",  # 44.1kHz sample rate
            "-y",  # Overwrite output file if it exists
            output_file
        ], check=True)
        
        # Clean up the temporary video file
        os.remove(temp_video)
        
        return output_file
                