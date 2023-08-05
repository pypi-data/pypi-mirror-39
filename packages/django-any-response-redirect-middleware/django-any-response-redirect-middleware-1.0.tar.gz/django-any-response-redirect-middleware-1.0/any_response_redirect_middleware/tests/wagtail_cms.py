from django.test import TestCase
from unittest import SkipTest


class RedirectMiddlewareTestsWithWagtailCMS(TestCase):

    @classmethod
    def setUpClass(self):
        super(RedirectMiddlewareTestsWithWagtailCMS, self).setUpClass()

        raise SkipTest("Skipping this test because we haven't written "
                       "wagtail cms tests yet.")
