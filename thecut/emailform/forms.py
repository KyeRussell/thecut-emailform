# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import settings
from collections import OrderedDict
from copy import copy
from django import forms
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template


class BaseEmailForm(forms.Form):
    """Base email form.

    Extends a standard Django :py:class:`~django.forms.Form` class with methods
    to send valid form data as an email.

    """

    from_email = settings.DEFAULT_FROM_EMAIL
    """The email address to send email to."""

    reply_to_emails = []
    """A list of email addresses to include in the ``Reply-To`` header of the
    email."""

    to_emails = settings.DEFAULT_TO_EMAILS
    """A list of email addresses to send the email to."""

    cc_emails = []
    """A list of email addresses to CC the email to."""

    email_context_data = {}
    """Data to pass to the template context when generating the email body."""

    email_headers = {}
    """Any custom headers to attach to the email."""

    email_subject = 'Enquiry'
    """The email's subject."""

    email_subject_prefix = settings.EMAIL_SUBJECT_PREFIX
    """The email's subject prefix. This is attached directly to the start of
    :py:attr:`thecut.emailform.forms.BaseEmailForm.email_subject` to form
    the email's subject."""

    email_template_name = 'emailform/email.txt'
    """The path to a Django template that should be used to generate the email
    body."""

    error_css_class = 'error'
    label_suffix = ''
    required_css_class = 'required'

    def get_email_alternatives(self, context):
        """Returns a list of tuples used to attach alternative content to the
        email.

        :returns: A list of tuples.
        :rtype: :py:class:`list`

        """

        return []

    def get_email_attachments(self):
        """Returns a list of attachments which will be added to the email.

        :returns: A list.
        :rtype: :py:class:`list`

        """

        return []

    def get_email_context_data(self, **kwargs):
        """Returns a data dictionary for use when rendering the email context.

        :returns: A dictionary.
        :rtype: :py:class:`dict`

        """

        context_data = {'form': self,
                        'form_fields': self.get_email_form_fields()}
        context_data.update(self.email_context_data)
        context_data.update(**kwargs)
        return context_data

    def get_email_form_fields(self):
        data = OrderedDict()
        for field in self:
            cleaned_data = self.cleaned_data.get(field.name, None)
            data.update({field.name: {'field': field, 'label': field.label,
                                      'cleaned_data': cleaned_data}})
        return data

    def get_email_headers(self):
        """Returns a dictionary of values for use as extra email headers.

        :returns: A dictionary of extra email headers.
        :rtype: :py:class:`dict`

        """

        return copy(self.email_headers)

    def get_email_kwargs(self, **kwargs):
        return kwargs

    def get_email_subject(self, subject=None):
        """Returns a string for use as an email's ``subject`` value.

        :keyword unicode subject: A string to join to the subject prefix.
        :returns: An email subject.
        :rtype: :py:class:`unicode`

        """

        if subject is None:
            subject = self.email_subject

        return '{prefix}{subject}'.format(prefix=self.email_subject_prefix,
                                          subject=subject)

    def get_email_template_name(self):
        """Returns a template name which will be used when rendering the email.

        :returns: A template name.
        :rtype: :py:class:`unicode`

        """

        return self.email_template_name

    def get_from_email(self):
        """Returns an email address for use as an email's ``from`` value.

        :returns: An email address.
        :rtype: :py:class:`unicode`

        """

        return self.from_email

    def get_reply_to_emails(self):
        """Returns a list of email addresses for use as an email's ``reply_to``
        value.

        :returns: List of email address strings.
        :rtype: :py:class:`list`

        """

        return copy(self.reply_to_emails)

    def get_to_emails(self):
        """Returns a list of email addresses for use as an email's ``to``
        value.

        :returns: List of email address strings.
        :rtype: :py:class:`list`

        """

        return copy(self.to_emails)

    def get_cc_emails(self):
        """Returns a list of email addresses for use as an email's ``cc``
        value.

        :returns: List of email address strings.
        :rtype: :py:class:`list`

        """

        return copy(self.cc_emails)

    def render_email_body(self, context, template_name=None):
        """Renders and returns content for use as an email's body text.

        :argument dict context: Context data dictionary to be used when
            rendering the template.
        :returns: Rendered body copy.
        :rtype: :py:class:`unicode`

        """

        if template_name is None:
            template_name = self.get_email_template_name()
        template = get_template(template_name)
        return template.render(context)

    def construct_email(self):
        """Construct an email for a valid form.

        :returns: Email message instance.
        :rtype: :py:class:`~django.core.mail.EmailMultiAlternatives`

        """

        assert self.is_valid()

        context = Context(self.get_email_context_data())
        email_kwargs = self.get_email_kwargs(
            subject=self.get_email_subject(),
            body=self.render_email_body(context),
            from_email=self.get_from_email(),
            reply_to=self.get_reply_to_emails(),
            to=self.get_to_emails(),
            cc=self.get_cc_emails(),
            headers=self.get_email_headers(),
            alternatives=self.get_email_alternatives(context),
            attachments=self.get_email_attachments(),
        )
        return EmailMultiAlternatives(**email_kwargs)

    def send_email(self, **kwargs):
        """Construct and send an email for a valid form."""

        mail = self.construct_email()
        return mail.send(**kwargs)
