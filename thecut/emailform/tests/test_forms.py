# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from test_app.forms import EmailForm
from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings
from mock import patch


class TestBaseEmailForm(TestCase):

    """Tests for the :py:class:`thecut.emailform.forms.BaseEmailForm`` form."""

    def setUp(self):
        self.form = EmailForm({'foo': 'bar'})

    # Base functionality

    def test_form_validates(self):
        """Form validates."""
        self.assertTrue(self.form.is_valid())

    def test_sends_email(self):
        """Send email."""
        self.form.send_email()
        self.assertEqual(len(mail.outbox), 1)

    # Defining email recipient

    @override_settings(EMAILFORM_DEFAULT_TO_EMAILS=['mail@example.com'])
    def test_sends_to_default_address(self):
        """Send email to default address (``EMAILFORM_DEFAULT_TO_EMAILS``)."""
        self.form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['mail@example.com'])

    def test_sends_to_overridden_address(self):
        """Send email to overridden address."""
        self.form.to_emails = ['override@example.com']
        self.form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['override@example.com'])

    # Defining email sender

    def test_sends_from_default_django_address(self):
        """Send email from default Django address (``DEFAULT_FROM_EMAIL``)."""
        self.form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, 'from@example.com')

    def test_sends_from_default_thecutemailform_address(self):
        """Send email from overridden address."""
        self.form.from_email = 'override@example.com'
        self.form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, 'override@example.com')

    # Defining reply-to

    def test_sends_with_empty_reply_to_by_default(self):
        """Send email with an empty ``reply-to`` header by default."""
        self.form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertFalse(mail.outbox[0].reply_to)

    def test_sends_with_reply_to(self):
        """Send email with a ``reply-to`` header when defined."""
        self.form.reply_to_emails = ['reply-to@example.com']
        self.form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].reply_to, ['reply-to@example.com'])

    # Defining CC (carbon copy)

    def test_sends_with_empty_cc_by_default(self):
        """Send email with an empty ``CC`` header by default."""
        self.form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertFalse(mail.outbox[0].cc)

    def test_sends_with_cc(self):
        """Send email with a ``CC`` header when defined."""
        self.form.cc_emails = ['cc@example.com']
        self.form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].cc, ['cc@example.com'])

    # Defining email subject

    def test_sends_with_sane_default_subject(self):
        """Send email with a sane default subject."""
        self.form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         '[thecut-emailform test suite] Enquiry')

    def test_sends_with_overridden_subject_prefix(self):
        """Send email with an overridden subject prefix."""
        self.form.email_subject_prefix = '[Overridden] '
        self.form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, '[Overridden] Enquiry')

    def test_sends_with_overridden_subject(self):
        """Send email with an overridden subject prefix."""
        self.form.email_subject = 'Overridden'
        self.form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         '[thecut-emailform test suite] Overridden')

    def test_sends_with_empty_subject(self):
        """Send email with an empty subject."""
        self.form.email_subject = ''
        self.form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         '[thecut-emailform test suite] ')

    def test_overriding_default_subject(self):
        """Send email with an overridden subject prefix."""
        self.form.email_subject_prefix = '[Overridden] '
        self.assertEqual(self.form.get_email_subject('Not default'),
                         '[Overridden] Not default')
