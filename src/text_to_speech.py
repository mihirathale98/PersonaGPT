import torch
from TTS.api import TTS


class TTS_Wrapper:
    def __init__(self,language="en"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
        self.language = language
    
    def get_speech(self, text, speaker_wav):
        wav = self.tts_model.tts(text=text, speaker_wav= speaker_wav, language=self.language)
        return wav
