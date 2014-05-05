#!/usr/bin/env python

import sys
import os


# Include folder with ./manage.py as module.
sys.path.insert(1, os.path.join(os.path.dirname(__file__)))

from otto import settings
from otto import modules
from otto.language import LanguageModel
from otto.conversation import Conversation

# If we are running this 'locally' then we
# use a faked microphone and speaker.
if '--local' in sys.argv:
    from otto.local_mic import Mic
else:
    from otto.mic import Mic


if __name__ == '__main__':

    try:
        command = sys.argv[1]
    except IndexError:
        print 'Usage'
        print '  manage.py compile'
        print '  manage.py run'
        exit()

    if command == 'compile':
        print 'Compiling language files ....'

        m = dir(modules)

        words = []
        for module_name in m:
            try:
                eval('words.extend(modules.%s.WORDS)' % module_name)
            except:
                pass  # module probably doesn't have the property

        words = list(set(words))

        # for spotify module
        words.extend(['MUSIC', 'SPOTIFY'])

        default_model = LanguageModel(settings.DEFAULT_MODEL_NAME)
        default_model.build(words)

    elif command == 'run':

        default_model = LanguageModel(settings.DEFAULT_MODEL_NAME)
        persona_model = LanguageModel(settings.PERSONA_MODEL_NAME)

        mic = Mic(
            default_decoder=default_model.get_decoder(),
            persona_decoder=persona_model.get_decoder(),
        )

        mic.say('How can I be of service?')

        conversation = Conversation('JASPER', mic, settings.USER_PROFILE)
        conversation.handleForever()
