=====
Usage
=====


Creating your form
-------------------

The main component of ``thecut-emailform`` is :py:class:`thecut.emailform.forms.BaseEmailForm`. To create an email form, create a :py:class:`thecut.emailform.forms.BaseEmailForm`.

.. autoclass:: thecut.emailform.forms.BaseEmailForm
  :show-inheritance:
  :members:


Customising your form
---------------------

There are two main ways of customising :py:class:`thecut.emailform.forms.BaseEmailForm`. You can either override the public getter methods (:py:meth:`thecut.emailform.forms.BaseEmailForm.get_email_subject`, :py:meth:`thecut.emailform.forms.BaseEmailForm.get_from_email`.etc) or you can alter the class attributes (e.g. :py:attr:`thecut.emailform.forms.BaseEmailForm.email_subject`, :py:attr:`thecut.emailform.forms.BaseEmailForm.from_email`) directly. For example::

    from thecut.emailform.forms import BaseEmailForm

    class MyEmailForm(BaseEmailForm):

        # Changing the email address / addresses the email is sent to.
        to_emails = ['email@example.com']

        # CHanging the email's subject
        def get_email_subject(self):
            return fetch_data()  # does not exist, just an example!

.. warning::
  If you choose to alter the instance attributes directly, the attribute assignment will occur when the *class* is first loaded (usually when the Django server starts up), with the result persisting until the server is shut down. If you're customising the form using 'dynamic' data (e.g. a value being loaded from a database) it's highly recommended that you override the relevant getter methods instead.


Using your form in a view
-------------------------

:py:class:`thecut.emailform.forms.BaseEmailForm` is just a regular :py:class:`django.forms.forms.Form`, so you use it in your views like you would any other form. Just call :py:meth:`thecut.emailform.forms.BaseEmailForm.send_email` when you want to send the email.

For exampe, we can use a :py:class:`django.views.generic.edit.FormView`::

    from .forms import MyEmailForm  # from the example above.
    from django.views.generic.edit import FormView

    class MyView(FormView):

        form_class = MyEmailForm

        def form_valid(self, form):
            form.send_email()
            return super(MyView, self).form_valid(form)
