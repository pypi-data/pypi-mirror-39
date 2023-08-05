from django.test import TestCase
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site

TEST_REDIRECTS = [
    {
        'old_path': '/page-that-doesnt-exist/',
        'new_path': 'https://www.foobar.com/the-other-location/',
    },
    {
        'old_path': '/another-page-that-doesnt-exist/',
        'new_path': '/a-local-url/',
    },
]


class BasicRedirectMiddlewareTests(TestCase):

    @classmethod
    def setUpClass(self):
        super(BasicRedirectMiddlewareTests, self).setUpClass()

        self.site = Site.objects.get_current()

        """ Add them to the db"""

        for redirect in TEST_REDIRECTS:
            instance = Redirect(
                site=self.site,
                **redirect
            )
            instance.save()

    def test_redirects_should_return_301(self):

        for redirect in TEST_REDIRECTS:

            response = self.client.get(redirect['old_path'])

            self.assertRedirects(response,
                                 redirect['new_path'],
                                 status_code=301,
                                 target_status_code=404,
                                 fetch_redirect_response=False)
