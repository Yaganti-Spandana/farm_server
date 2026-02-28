import socket
from django.core.mail.backends.smtp import EmailBackend

class IPv4EmailBackend(EmailBackend):
    def open(self):
        self.connection = None
        try:
            self.connection = self.connection_class(
                (self.host, self.port),
                timeout=self.timeout,
                source_address=None,
            )
            return True
        except OSError:
            return False