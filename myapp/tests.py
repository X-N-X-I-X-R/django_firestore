from django.test import TestCase
from django.core import mail

class EmailTestCase(TestCase):
    def test_send_email(self):
        mail.send_mail(
            'Hello from Django',
            'This is a test email.',
            'the-farm@outlook.co.il',
            ['nirstam@gmail.com'],
            fail_silently=False,
        )

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify the subject of the first message.
        self.assertEqual(mail.outbox[0].subject, 'Hello from Django')