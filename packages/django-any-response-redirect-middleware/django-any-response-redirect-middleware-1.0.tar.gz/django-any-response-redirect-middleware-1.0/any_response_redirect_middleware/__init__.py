from django.contrib.redirects.middleware import RedirectFallbackMiddleware
from django.http import HttpResponseGone, HttpResponsePermanentRedirect


class AnyResponseCodeRedirectMiddleware(RedirectFallbackMiddleware):
    """ A subclass of the redirect middleware that will apply
        redirects to all responses, not just 404s. """

    def process_response(self, request, response):
        original_status_code = response.status_code

        """ Temporarily set the status code for 200 requests to
            404 to make the base middleware check for the
            existence of a redirect """
        if response.status_code == 200:
            response.status_code = 404

        """ Let the base middleware process it and get
            a response """
        response = super(
            AnyResponseCodeRedirectMiddleware,
            self
        ).process_response(request, response)

        """ If the base middleware doesn't return an HttpsResponseGone or
            HttpResponsePermanentRedirect class, set the response to back
            to what it was originally """

        if not any([
            isinstance(response, HttpResponseGone),
            isinstance(response, HttpResponsePermanentRedirect)
        ]):
            response.status_code = original_status_code

        return response