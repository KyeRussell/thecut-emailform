================
thecut-emailform
================


.. image:: https://travis-ci.org/thecut/thecut-emailform.svg
    :target: https://travis-ci.org/thecut/thecut-emailform

.. image:: https://codecov.io/github/thecut/thecut-emailform/coverage.svg
    :target: https://codecov.io/github/thecut/thecut-emailform

.. image:: https://readthedocs.org/projects/thecut-emailform/badge/?version=latest
    :target: http://thecut-emailform.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Django class-based view and form to send enquiry emails.


Features
--------

* Send emails using a regular Django form.
* Use Django templates to generate your email's body.
* Send HTML / multi-part emails.
* Add email headers like ``Cc``, ``Bcc``, and ``Reply-To``.


Documentation
-------------

The full documentation is at https://thecut-emailform.readthedocs.org.


Quickstart
----------

1. Install ``thecut-emailform`` using the :ref:`installation`.

2. Create a new form based on :py:class:`thecut.emailform.forms.BaseEmailForm`::

    class MyEmailForm(BaseEmailForm):

        # Changing the email address / addresses the email is sent to.
        to_emails = ['email@example.com']

3. Use your new form in a view::

    class MyView(FormView):

        form_class = MyEmailForm

        def form_valid(self, form):
            form.send_email()
            return super(MyView, self).form_valid(form)


Credits
-------

See ``AUTHORS.rst``.
