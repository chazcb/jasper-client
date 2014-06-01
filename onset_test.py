import pygst
pygst.require('0.10')

import gst

if __name__ == "__main__":

    pipeline = gst.parse_launch(
        'autoaudiosrc ! audioconvert ! audioresample '
        + '! vader name=vad auto-threshold=true '
        + '! pocketsphinx name=asr ! fakesink')
