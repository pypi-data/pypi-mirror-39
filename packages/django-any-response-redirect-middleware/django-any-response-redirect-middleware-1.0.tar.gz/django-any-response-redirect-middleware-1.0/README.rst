django-any-response-redirect-middleware
---------------------------------------

A subclass of Django's RedirectFallbackMiddleware that will catch any response code, not just 404s.

Installation::

    pip install django-any-response-redirect-middleware

Setup::

    MIDDLEWARE = [
        ...middleware classes,
        'any_response_redirect_middleware.AnyResponseCodeRedirectMiddleware',
    ]

Run tests::

    ./manage.py test any_response_redirect_middleware.tests






