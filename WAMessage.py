from WAMediaType import WAMediaType
from datetime import datetime

class WAMessage:

    def __init__(self, id, remote_jid, from_me, data, timestamp,
                 media_type, media_caption, media_duration, file_name,
                 latitude, longitude, quoted_message, is_link):
        self.id = id
        self.remote_jid = remote_jid
        self.from_me = from_me
        self.data = data if data != None else ""
        self.timestamp = timestamp
        try:
            self.media_type = WAMediaType(int(media_type))
        except ValueError:
            self.media_type = WAMediaType.UNKNOWN
        self.media_caption = media_caption if media_caption != None else ""
        self.media_duration = media_duration
        self.file_name = file_name
        self.latitude = latitude
        self.longitude = longitude
        self.quoted_message = quoted_message
        self.is_link = is_link


    def posix_to_human(self, timestamp):
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def toString(self):
        r = self.id + " " + self.posix_to_human(self.timestamp / 1000) + "; "

        r = r + ("   ME: " if self.from_me else "OTHER: ")
        
        if self.quoted_message:
            r = r + "[ Quote from " + \
                self.posix_to_human(self.quoted_message.timestamp / 1000) + \
                ": " + self.quoted_message.id + "]; "

        if self.media_type == WAMediaType.TEXT:
            if self.is_link:
                r = r + "[ Link: "
                if len(self.media_caption) > 0:
                    r = r + self.media_caption + "; "

                r = r + self.data + " ]"
            else:
                r = r + self.data 

        if self.media_type == WAMediaType.IMAGE:
            r = r + "[ Image: " + self.file_name
            if len(self.media_caption) > 0:
                r = r + "; " + self.media_caption

            r = r + self.data + " ]"

        if self.media_type == WAMediaType.AUDIO:
            r = r + "[ Audio: " + str(self.media_duration) + "s; " + self.file_name + " ]"
            
        if self.media_type == WAMediaType.VIDEO:
            r = r + "[ Video: " + self.file_name
            if len(self.media_caption) > 0:
                r = r + "; " + self.media_caption

            r = r + self.data + " ]"
            
        if self.media_type == WAMediaType.CONTACT:
            r = r + "[ Contact ]"
        if self.media_type == WAMediaType.LOCATION or self.media_type == WAMediaType.LIVE_LOCATION:
            r = r + "[ Location: " + self.latitude + ", " + self.longitude + " ]"
        if self.media_type == WAMediaType.LIVE_LOCATION:
            pass
        if self.media_type == WAMediaType.GIF:
            r = r + "[ Image (gif/mp4): "
            if len(self.media_caption) > 0:
                r = r + "; " + self.media_caption

            r = r + self.data + " ]"

        return r
