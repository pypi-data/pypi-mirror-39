from django.test import TestCase
from cms.api import create_page
from cms import constants
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from unittest import SkipTest


class RedirectMiddlewareTestsWithDjangoCMS(TestCase):

    @classmethod
    def setUpClass(self):
        super(RedirectMiddlewareTestsWithDjangoCMS, self).setUpClass()

        try:
            import cms
        except Exception:
            raise SkipTest("Skipping this test because it "
                           "doesn't look like Django CMS is installed")

        self.site = Site.objects.get(id=1)
        self.site.name = 'testserver'
        self.site.domain = 'testserver'
        self.site.save()

        self.home_page = create_page(
            'home',
            constants.TEMPLATE_INHERITANCE_MAGIC,
            'en-us',
            published=True,
            site=self.site
        )

        self.non_redirected_page = create_page(
            'Non Redirected Page',
            constants.TEMPLATE_INHERITANCE_MAGIC,
            'en-us',
            slug='non-redirected-page',
            published=True,
            parent=self.home_page,
            site=self.site
        )

        self.redirected_page = create_page(
            'Redirected Page',
            constants.TEMPLATE_INHERITANCE_MAGIC,
            'en-us',
            slug='redirected-page',
            published=True,
            parent=self.home_page,
            site=self.site
        )

        self.nested_redirected_page = create_page(
            'Nested Redirected Page',
            constants.TEMPLATE_INHERITANCE_MAGIC,
            'en-us',
            slug='nested-redirected-page',
            published=True,
            parent=self.redirected_page,
            site=self.site
        )

        self.redirect = Redirect(
            site=self.site,
            old_path=self.get_relative_url(
                self.redirected_page.get_absolute_url()
            ),
            new_path='/the-new-location/'
        )
        self.redirect.save()

        self.nested_redirect = Redirect(
            site=self.site,
            old_path=self.get_relative_url(
                self.nested_redirected_page.get_absolute_url()
            ),
            new_path='/the-other-location/',
        )
        self.nested_redirect.save()

        self.non_existent_page_redirect = Redirect(
            site=self.site,
            old_path='/page-that-doesnt-exist/',
            new_path='/the-other-location/',
        )
        self.non_existent_page_redirect.save()

    def test_redirected_page_will_return_301(self):

        response = self.make_request(
            self.get_relative_url(
                self.redirected_page.get_absolute_url()
            ),
        )

        self.assertRedirects(response,
                             self.redirect.new_path,
                             status_code=301,
                             fetch_redirect_response=False)

    def test_non_existent_page_will_return_301(self):

        response = self.make_request(
            self.non_existent_page_redirect.old_path,
        )

        self.assertRedirects(response,
                             self.nested_redirect.new_path,
                             status_code=301,
                             target_status_code=404,
                             fetch_redirect_response=False)

    def test_non_redirected_page_will_return_200(self):

        response = self.make_request(
            self.get_relative_url(
                self.non_redirected_page.get_absolute_url()
            ),
        )
        self.assertEqual(response.status_code, 200)

    def test_nested_redirected_page_will_actually_redirect(self):

        response = self.make_request(
            self.get_relative_url(
                self.nested_redirected_page.get_absolute_url()
            ),
        )

        self.assertRedirects(response,
                             self.nested_redirect.new_path,
                             status_code=301,
                             target_status_code=200,
                             fetch_redirect_response=False)

    def make_request(self, url):

        return self.client.get(
            url,
            {},
            SERVER_NAME=self.site.domain,
            ACCEPT_LANGUAGE='en-US,en'
        )

    @classmethod
    def get_absolute_url(self, relative_url):

        return 'http://%s%s' % (self.site.domain, relative_url)

    @classmethod
    def get_relative_url(self, absolute_url):

        return absolute_url.replace('http://%s' % self.site.domain, '')
