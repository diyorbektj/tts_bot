import torch
import sounddevice as sd
import time
import os
import soundfile as sf

language = 'uz'
model_id = 'v3_uz'
sample_rate = 48000
speaker = 'dilnavoz'
put_accent = True
put_yo = True
device = torch.device('cpu')

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)

def va_speak(what: str, number: int):
    audio_paths = model.save_wav(text=what+"..........  ",
                             speaker=speaker,
                             sample_rate=sample_rate)
                           
    data, samplerate = sf.read('test.wav')
    sf.write(str(number)+'.ogg', data, samplerate)
    os.remove("test.wav")
