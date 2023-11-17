# PRFrogService
This is essentially the Coqui voiceover service that should works with Coqui Studio API. Created a new repository, to share. 

## Example

```python

os.environ["COQUI_STUDIO_TOKEN"] = "________________________________"
is_coqui_available = os.environ.get("COQUI_STUDIO_TOKEN")
# or XTTS
models = TTS(cs_api_model="V1").list_models()
class MyAwesomeScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(PRFrogService(model_name="coqui_studio/multilingual/Joshua Graham/V1",
            gpu=True
            ))

        # self.set_speech_service(PyTTSX3Service())
        with self.voiceover(text="This circle is drawn as I speak.",language="en") as tracker:
            self.play(Create(Circle()), run_time=tracker.duration)
        self.wait()
```
