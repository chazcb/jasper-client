from notifier import Notifier
from brain import Brain


class Conversation(object):

    def __init__(self, persona, mic, profile):
        self.persona = persona
        self.mic = mic
        self.profile = profile
        self.brain = Brain(mic, profile)
        self.notifier = Notifier(profile)

    def delegateInput(self, text):
        """A wrapper for querying brain."""
        self.brain.query(text)

    def handleForever(self):
        """Delegates user input to the handling function when activated."""
        while True:

            # Print notifications until empty
            notifications = self.notifier.getAllNotifications()
            for notif in notifications:
                print notif

            try:
                threshold, transcribed = self.mic.passiveListen(self.persona)
            except:
                continue

            if threshold:
                input = self.mic.activeListen(threshold)
                if input:
                    self.delegateInput(input)
                else:
                    self.mic.say("Pardon?")
