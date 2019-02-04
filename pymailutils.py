import imaplib
import poplib
import time

class Imap:
    def __init__(self, hostname, port=None, username=None, password=None):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

        if port == 993:
            try:
                self.conn = imaplib.IMAP4_SSL(hostname, port)
                if 'STARTTLS' in self.conn.capabilities:
                    print("trovato")
            except:
                self.conn = False
        elif port == 143:
            try:
                self.conn = imaplib.IMAP4(hostname, port)
            except:
                self.conn = False

        self.prelogincapabilities = self.conn.capabilities
        self.preloginwelcome = self.conn.welcome

        try:
            self.conn.login(username, password)
            self.loginfailed = False
        except:
            self.loginfailed = True

    def __enter__(self):
        return self

    def folders(self):
        folders = []
        status, imap_folders = self.conn.list()
        for folder in imap_folders:
            folder_name = folder.decode("utf-8").split('"."')[-1].strip()
            folders.append(folder_name)
        return status, folders

    def has_mailbox(self, mailbox):
        typ, folders = self.folders()
        found = False
        for folder in folders:
            if folder.endswith(mailbox):
                found = True
        return found

    def select(self, mailbox):
        return self.conn.select(mailbox)

    def search(self, pattern, mailbox="INBOX", timeout=10):
        time.sleep(1)
        count = 1
        uids = []
        # This loop is needed because the message can be arrive after some seconds to the run test
        while count < timeout and len(uids) == 0:
            self.conn.select(mailbox)
            status, data = self.conn.search(None, pattern)
            for msg in data[0].split():
                # With this way can you check empty byte string
                if len(msg) > 0:
                    uids.append(msg.decode())
            count=count+1
            time.sleep(1)
        return uids

    def fetch(self, mailbox='INBOX'):
        self.select(mailbox)
        self.conn.fetch()
    def fetch_with_uid(self, uid, mailbox="INBOX"):
        status, message = self.conn.fetch(uid, '(RFC822)')
        return message

    def create_folder_and_subscribe(self, folder):
        self.conn.create(folder)
        self.conn.subscribe(folder)

    def delete_folder_and_unsubscribe(self, folder):
        self.conn.unsubscribe(folder)
        self.conn.delete(folder)

    def delete(self, pattern, mailbox="INBOX"):
        data = self.search(pattern)
        for msg in data:
            self.conn.store(msg, '+FLAGS', '\\Deleted')
        self.conn.expunge()

    def subscriptions(self):
        subscriptions = []
        status, imap_subscriptions = self.conn.lsub()
        for sub in imap_subscriptions:
            subscriptions.append(sub.decode("utf-8").split('"."')[-1].strip())
        return status, subscriptions

    def logout(self):
        self.conn.logout()

    def __exit__(self, type, value, traceback):
        self.logout()
class Pop3:
    def __init__(self, server, port=None, username=None, password=None, timeout=10):
        self.server = server
        self.port = port
        self.username = username
        self.password = password

        if port == 995:
            try:
                self.conn = poplib.POP3_SSL(server, port)
            except:
                self.fail
        elif port == 110:
            try:
                self.conn = poplib.POP3(server, port)
            except:
                self.fail

        self.preloginwelcome = self.conn.welcome.decode("ascii")

        try:
            self.user = self.conn.user(username)
            self.auth = self.conn.pass_(password)
        except (poplib.error_proto) as e:
            self.err = e.args[0].decode("ascii")

    def __enter__(self):
        return self

    def stat(self):
            return self.conn.stat()

    def retr(self, which):
            response, line, octets = self.conn.retr(which)
            return response.decode('ascii'), line, octets

    def search(self, subject, timeout=30):
        # This method (implicitly) implements a pop3 searching by Subject
        # If usefull we can easily improve it adding a case for searching by From To (Subject) Date headers
        #
        time.sleep(1)
        count = 1
        # wait-for-message-in-pop3-mailbox loop
        while count < timeout:
            messages_ids = [ int(m.split()[0]) for m in self.conn.list()[1]]
            for id in messages_ids:
                response, lines, octets = self.conn.top(id, 0)
                for line in lines:
                    linestr = line.decode('ascii')
                    if linestr.startswith('Subject:'):
                        subject_header = linestr.partition('Subject: ')[2]
                        if subject == subject_header:
                            return id
            count=count+1
            time.sleep(1)
        return False

    def dele(self, which):
            return self.conn.dele(which).decode('ascii')

    def __exit__(self, type, value, traceback):
        self.conn.quit()

class Email:
    def download_attachment(attachment, download_dir="/tmp"):
        if not attachment:
            print("vuoto")
            return None

            filename = attachment.get_filename()
            filepath = download_dir + '/' + filename
            if not os.path.isfile(filepath):
                fp = open(filepath, 'wb')
                fp.write(attachment.get_payload(decode=True))
                fp.close()

                return(filepath)

    def get_body(self,email_as_text=None):
        msg = email.message_from_string(email_as_text)
        if msg.is_multipart():
            for payload in msg.get_payload():
                print_payload(payload)
                return(paylod)
        else:
            for part in msg.walk():
                if part.get_content_type():
                    body = str(part.get_payload())
                    return(body)
