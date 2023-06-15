import traceback

import ffmpeg
import numpy as np
import whisper

from gpt4all import GPT4All
from numpy import ndarray
from TTS.api import TTS
from base64 import b64decode, b64encode

from talkItApp.models import Teacher, User


class InferenceService:
    instance = None

    @staticmethod
    def get_instance():
        if InferenceService.instance is None:
            InferenceService.instance = InferenceService()

        return InferenceService.instance

    def __init__(self):
        self._whisper = whisper.load_model("small")
        self._gpt4all = GPT4All('ggml-gpt4all-l13b-snoozy')
        self._tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False, gpu=False)
        print(self._tts.speakers)
        print(self._tts.languages)

    def get_response(self, audio, user: User, teacher: Teacher):
        try:
            question = self._do_stt(self._load_audio(audio), user)
            answer_text = self._genterate_response(question, user, teacher)
            answer_voice = self._generate_audio(answer_text)
        except Exception as e:
            print(e)
            return None

        return answer_voice, answer_text

    def _do_stt(self, audio: ndarray, user: User) -> str:
        result = self._whisper.transcribe(audio, language='en')

        text = result['text'].strip()
        print(f'\n\033[92m{user.username} ha preguntado: "{text}"\033[0m\n')

        return text

    def _genterate_response(self, question, user: User, teacher: Teacher):
        user_msg = {'role': 'user', 'content': question}

        msgs = list(eval(teacher.last_msgs if teacher.last_msgs is not None else '[]')) # PELIGROSÍSIMO: En un caso práctico, hay que incluir comprobaciones, esto se podría usar como exploit.
        if not msgs:
            msgs.append({
                'role':
                    'system',
                'content':
                    f'''
                    ### Instruction: 
                    Your name is {teacher.name}, and you are a private English teacher. The name of your student is {user.username}. Your goal is to answer your students\' questions, and help them correct their grammatical errors.
                    
                    {teacher.prompt}
    
                    The prompt below is a conversation with your student; correct their mistakes and / or answer their questions. Elaborate your answer.'
    
                    \n### Prompt:  
                    ''' # El prompt debería ser traducido al inglés. Esto se puede hacer mediante el propio gpt4all, pero eso queda para una futura mejora.
            })

        msgs.append(user_msg)

        teacher_msg = self._gpt4all.chat_completion(msgs, verbose=False, streaming=False, default_prompt_header=False)['choices'][0]['message']
        msgs.append(teacher_msg)

        teacher.last_msgs = str(msgs)
        teacher.save()

        text = teacher_msg['content'].replace('"', '\"').strip()
        print(f'\n\033[92m{teacher.name} ha respondido: "{text}"\033[0m\n')
        return text

    @staticmethod
    def _load_audio(file_bytes: bytes, sr: int = 16_000) -> np.ndarray:
        """
        Use file's bytes and transform to mono waveform, resampling as necessary
        Parameters
        ----------
        file_bytes: bytes
            The bytes of the audio file
        sr: int
            The sample rate to resample the audio if necessary
        Returns
        -------
        A NumPy array containing the audio waveform, in float32 dtype.
        """

        file_bytes = b64decode(file_bytes)

        try:
            # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
            # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
            out, _ = (
                ffmpeg.input('pipe:', threads=0)
                .output("pipe:", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
                .run_async(pipe_stdin=True, pipe_stdout=True)
            ).communicate(input=file_bytes)

        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

        return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

    def _generate_audio(self, message):
        try:
            self._tts.tts_to_file(message, file_path='./temp.wav')

            with open('./temp.wav', 'rb') as f:
                return b64encode(f.read()).decode('ascii')
        except Exception as e:
            traceback.print_exc()


InferenceService.get_instance()
