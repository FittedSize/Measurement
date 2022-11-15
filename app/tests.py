from django.test import TestCase
from .models import Trouser
from django.core.exceptions import ValidationError
from django.urls import resolve
from django.http import HttpRequest
from .views import home


class TestTrouser(TestCase):
    def setUp(self):
        trouser_data_1 = dict(length=40, waist=30.4, thigh=10.5, ankle=10, calf=5)
        self.valid_trouser = Trouser(**trouser_data_1)

        self.invalid_data = dict(length=-40, waist=30.4, thigh=10.5, ankle=-10, calf=5)
        self.valid_trouser.save()

    def test_trouser_counts(self):
        counts = Trouser.objects.count()
        self.assertEqual(counts, 1)

    def test_lenght(self):
        t = self.valid_trouser
        self.assertEqual(t.length, 40)

    def test_raise_validation_error(self):
        data = Trouser(**self.invalid_data)
        with self.assertRaises(ValidationError):
            data.full_clean()


class HomePageTest(TestCase):
    def test_root_resolve_to_index(self):
        found = resolve("/")
        self.assertEqual(found.func, home)

    def test_measurement_in_homepage(self):
        request = HttpRequest()
        response = home(request)
        content = response.content.decode("utf8")
        pattern = "[Mm]easurement"
        self.assertRegexpMatches(content, pattern)
