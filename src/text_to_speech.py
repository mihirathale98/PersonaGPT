import torch
from TTS.api import TTS
import textwrap
import numpy as np

class TTS_Wrapper:
    def __init__(self, language="en", max_chars=250):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
        self.language = language
        self.max_chars = max_chars  # Limit per chunk

    def split_text(self, text):
        """
        Split text into smaller chunks based on the max character limit.
        Tries to split at sentence boundaries for better continuity.
        """
        text_list = textwrap.wrap(text, self.max_chars, break_long_words=False, replace_whitespace=False)
        return [text.strip() for text in text_list]

    def get_speech(self, texts, speaker_wavs):
        """
        Generate speech for a batch of texts and speaker WAVs, handling long text by splitting it.
        
        Args:
            texts (List[str]): A list of text strings to synthesize.
            speaker_wavs (List[str]): A list of speaker WAV file paths corresponding to each text.
        
        Returns:
            List[numpy.ndarray]: A list of generated waveforms for each text or chunked text.
        """
        assert len(texts) == len(speaker_wavs), "The number of texts and speaker WAVs must match."
        
        batched_wavs = []
        for text, speaker_wav in zip(texts, speaker_wavs):
            # Split long text into chunks
            text_chunks = self.split_text(text)
            wav_chunks = []
            for chunk in text_chunks:
                wav_chunk = self.tts_model.tts(text=chunk, speaker_wav=speaker_wav, language=self.language)
                wav_chunks.append(wav_chunk)
            
            # Concatenate the chunks if needed
            batched_wavs.append(self.concatenate_wavs(wav_chunks))
        
        return batched_wavs

    def concatenate_wavs(self, wav_chunks):
        """
        Concatenate multiple audio chunks into one.
        """
        #expected Tensor as element 0 in argument 0, but got list
        wav_chunks = np.array(wav_chunks)
        return np.concatenate(wav_chunks)


