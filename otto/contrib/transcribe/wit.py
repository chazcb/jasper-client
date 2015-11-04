import requests
from otto import settings


class WitSTT(object):

    url = 'https://api.wit.ai/speech'

    def transcribe(self, wav):
        response = requests.post(
            self.url,
            data=wav,
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

        print response.content
        print response.request.headers

        json = response.json()
        return json['_text']
