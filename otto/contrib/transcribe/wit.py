import requests
import wave

from contextlib import closing
from tempfile import TemporaryFile

from otto import settings


class WitSTT(object):

    url = 'https://api.wit.ai/speech'

    def transcribe(self, data):

        tmp_file = TemporaryFile()

        with closing(wave.open(tmp_file, 'wb')) as w:
            w.setnchannels(1)
            w.setsampwidth(2L)
            w.setframerate(16000)
            # `data` is a stream object, I should be able to
            # pass it to request.post raw and stream the audio
            # to wit.ai.
            w.writeframes(b''.join(data))

        tmp_file.seek(0)

        response = requests.post(
            self.url,
            data=tmp_file,
            params={
                'v': 20141022,
                # 'encoding': 'floating-point',
                # 'bits': 16,
                # 'rate': '16k',
                # 'endian': 'little'
            },
            headers={
                'Authorization': 'Bearer %s' % settings.WIT_TOKEN,
                'Content-Type': 'audio/wav',
            },
        )
        tmp_file.close()

        print response.content
        print response.request.headers

        json = response.json()
        return json['_text']
