import sqlite3
import sys

from WAChat import WAChat
from WAMessage import WAMessage

class WAExporter:

    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName)


    def getChats(self):
        """
        Get all WAChat's in the DB.
        """
        c = self.conn.cursor();
        c.execute("""
        SELECT chat_list.key_remote_jid,
            chat_list.subject,
            chat_list.creation,
            MAX(messages.timestamp)
        FROM chat_list
            LEFT OUTER JOIN messages ON messages.key_remote_jid = chat_list.key_remote_jid
        GROUP BY chat_list.key_remote_jid, chat_list.subject, chat_list.creation
        ORDER BY MAX(messages.timestamp) DESC
        """)
        response = c.fetchall()
        typed = []
        for i in range(0, len(response)):
            typed.append(WAChat(
                response[i][0],
                response[i][1],
                response[i][2],
                response[i][3]
            ))
        return typed


    def getChatMessages(self, chat_id):
        """
        Returns all WAMessage's from the database for key_remote_jid. Resolves 
        quoted messages one layer deep (as WA itself does).
        """
        c = self.conn.cursor();
        c.execute("""
        SELECT messages.key_id,
               messages.key_remote_jid,
               messages.key_from_me,
               messages.DATA,
               messages.TIMESTAMP,
               messages.media_wa_type,
               messages.media_caption,
               messages.media_duration,
               messages.latitude,
               messages.longitude,
               messages_quotes.key_id,
               messages_links._id
          FROM messages
                 LEFT JOIN messages_quotes
                     ON messages.quoted_row_id > 0 AND messages.quoted_row_id = messages_quotes._id
                 LEFT JOIN messages_links
                     ON messages._id = messages_links.message_row_id
         WHERE messages.key_remote_jid = ?
         ORDER BY messages.timestamp ASC
        """, (chat_id, ))
        response = c.fetchall()
        typed = []
        for i in range(0, len(response)):
            quoted_message = self.getMessageById(response[i][10]) \
                if response[i][10] != None else None
            
            typed.append(WAMessage(
                response[i][0], response[i][1], response[i][2], response[i][3], response[i][4],
                response[i][5], response[i][6], response[i][7], "", response[i][8], response[i][9],
                quoted_message, response[i][11],
            )) # TODO filename
        return typed

    def getMessageById(self, id):
        """
        Returns a single WAMessage from the DB by its key_id. Does not retrive any
        quoted messages or links, as this is intended to be used to retrieve 
        quoted_messages from `self.getChatMessages()`
        """
        c = self.conn.cursor();
        c.execute("""
        SELECT messages.key_id,
               messages.key_remote_jid,
               messages.key_from_me,
               messages.DATA,
               messages.TIMESTAMP,
               messages.media_wa_type,
               messages.media_caption,
               messages.media_duration,
               messages.latitude,
               messages.longitude
         FROM messages
         WHERE messages.key_id = ?
        """, (id, ))
        response = c.fetchone()
        typed = WAMessage(
            response[0], response[1], response[2], response[3], response[4],
            response[5], response[6], response[7], "", response[8], response[9],
            None, False
        ) # TODO filename
        return typed


    def checkArgv(self):
        if len(sys.argv) < 2:
            print('Usage: waexport.py [database]')
            exit(1)



def main():
    # checkArgv()
    wae = WAExporter('..\\messages.decrypted.db')
    # print(list(map(lambda c: c.creation, wae.getChats())))

    # print(wae.getMessageById('43AAFF52B7E9DF3D248EEA3D7B97B78D').__dict__)

    for m in wae.getChatMessages('4915751163903@s.whatsapp.net'):
        # if m.data != None: print(m.data.encode('ascii', 'ignore'))
        print(m.toString().encode('ascii', 'ignore'))
        # if m.quoted_message != None: print(m.quoted_message.data.encode('ascii', 'ignore'))
        pass



main()
