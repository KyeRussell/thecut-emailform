# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.views import generic
from project.contact.forms import EnquiryForm


class EmailFormView(generic.FormView):
    
    def form_valid(self, form, *args, **kwargs):
        form.send_email()
        return super(EmailFormView, self).form_valid(form, *args, **kwargs)

