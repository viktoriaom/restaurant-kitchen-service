from django.test import TestCase

from kitchen.forms import CookCreationForm


class FormsTest(TestCase):
    def test_cook_creation_form_with_add_fields_is_valid(self):
        form_data = {
            "username": "test_username",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test First",
            "last_name": "Test Last",
            "years_of_experience": 2354
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"], form_data["username"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"], form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"], form_data["last_name"]
        )
        self.assertEqual(
            form.cleaned_data["years_of_experience"],
            form_data["years_of_experience"]
        )
