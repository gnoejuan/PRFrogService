from pathlib import Path
from manim import logger
from manim_voiceover.helper import prompt_ask_missing_package, remove_bookmarks, wav2mp3
from manim_voiceover.services.base import SpeechService
from icecream import ic

try:
    from TTS.api import TTS
except ImportError:
    logger.error("Missing packages. Run `pip install TTS` to use PRFrogService.")

DEFAULT_MODEL = "tts_models/en/ljspeech/tacotron2-DDC"

class PRFrogService(SpeechService):
    """Custom speech service using the Coqui TTS framework.
    Default model: ``tts_models/en/ljspeech/tacotron2-DDC``.
    """

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        config_path: str = None,
        vocoder_path: str = None,
        vocoder_config_path: str = None,
        progress_bar: bool = True,
        gpu=False,
        speaker_idx=0,
        language_idx=0,
        **kwargs,
    ):
        self.tts = TTS(
            model_name=model_name,
            config_path=config_path,
            vocoder_path=vocoder_path,
            vocoder_config_path=vocoder_config_path,
            progress_bar=progress_bar,
            gpu=gpu,
        )

        # Check and assign speaker and language
        self.speaker = None
        self.language = None

        if hasattr(self.tts, 'speakers') and self.tts.speakers:
            self.speaker = self.tts.speakers[speaker_idx] if len(self.tts.speakers) > speaker_idx else None

        if hasattr(self.tts, 'languages') and self.tts.languages:
            self.language = self.tts.languages[language_idx] if len(self.tts.languages) > language_idx else None

        self.init_kwargs = kwargs
        prompt_ask_missing_package("TTS", "TTS>=0.13.3")
        SpeechService.__init__(self, **kwargs)

    def generate_from_text(
        self, text: str, cache_dir: str = None, path: str = None, language: str = None, **kwargs
    ) -> dict:
        if cache_dir is None:
            cache_dir = self.cache_dir

        input_text = remove_bookmarks(text)
        input_data = {"input_text": text, "service": "coqui"}

        cached_result = self.get_cached_result(input_data, cache_dir)
        if cached_result is not None:
            return cached_result

        if path is None:
            audio_path = self.get_audio_basename(input_data) + ".mp3"
        else:
            audio_path = path

        if not kwargs:
            kwargs = self.init_kwargs
            
        language = language

        output_path = str(Path(cache_dir) / audio_path)
        wav_path = Path(output_path).with_suffix(".wav")
        wav_path_str = str(wav_path)  # Convert Path object to string
        ic(language)
        
        # Text to speech to a file
        self.tts.tts_to_file(
            text=input_text,
            speaker=self.speaker,
            language=language,
            file_path=wav_path_str,
        )
        wav2mp3(wav_path, output_path)
        
        ic(output_path)
        # ic(os.path.exists(output_path))

        json_dict = {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
            # "word_boundaries": word_boundaries,
        }

        return json_dict
