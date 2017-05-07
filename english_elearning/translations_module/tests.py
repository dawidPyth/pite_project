# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from django.core import mail
from django.test import TestCase


class EmailTest(TestCase):
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
    def test_send_email(self):
        mail.send_mail('Subject here', 'Here is the message.',
            'python.projekt@o2.pl', ['jan125djw@gmail.com'],
            fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')
