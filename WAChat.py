
class WAChat:

    def __init__(self, key_remote_jid, subject, creation,
                 last_message_timestamp):
        self.key_remote_jid = key_remote_jid
        self.subject = subject
        self.creation = creation
        self.last_message_timestamp = last_message_timestamp
