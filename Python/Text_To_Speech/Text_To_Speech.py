import torch
from scipy.io.wavfile import write
import uberduck
class Text_To_Speech_Uberduck_Wav_Output:
    def __init__(self):
        self.client = uberduck.UberDuck("pub_aunuanvcxyzyaesdxg", "pk_80032937-33af-41ba-92c4-fd42d5277b9f")
        self.speech_model = "siri-female-british"

    def process(self, text, output_file):
        return self.client.speak(text, self.speech_model, play_sound = False, file_path=output_file)
    def __call__(self, text, output_file):
        return self.process(text, output_file)
class Text_To_Speech_Local_Wav_Output:
    def __init__(self):
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.tacotron2 = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_tacotron2', model_math='fp16')
        self.tacotron2 = self.tacotron2.to(device)
        self.tacotron2.eval()

        self.waveglow = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_waveglow', model_math='fp16')
        self.waveglow = self.waveglow.remove_weightnorm(self.waveglow)
        self.waveglow = self.waveglow.to('cuda')
        self.waveglow.eval()

        self.utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_tts_utils')

        self.rate = 22050

    def process(self, text, output_file):
        if len(text) == 0:
            return
        print(len(text))

        sequences, lengths = self.utils.prepare_input_sequence([text])
        with torch.no_grad():
            mel, _, _ = self.tacotron2.infer(sequences, lengths)
            audio = self.waveglow.infer(mel)
        audio_numpy = audio[0].data.cpu().numpy()

        write(output_file, self.rate, audio_numpy)

    def __call__(self, text, output_file):
        self.process(text, output_file)


if __name__ == "__main__":
    tts = Text_To_Speech_Local_Wav_Output()
    tts("This is a test", "./temp.wav")