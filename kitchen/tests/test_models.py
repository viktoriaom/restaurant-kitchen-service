from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType, Dish, Ingredient


# Create your tests here.
class ModelsTests(TestCase):
    def create_dishtype_to_test(self):
        dishtype = DishType.objects.create(name="dishtype_test")
        return dishtype

    def create_cook_to_test(self):
        cook = get_user_model().objects.create_user(
            username="cook_test",
            password="pass_cook_test",
            first_name="Firstname_cook_test",
            last_name="Lastname_cook_test",
            years_of_experience=10,
        )
        return cook

    def create_dish_to_test(self):
        dishtype = self.create_dishtype_to_test()
        cook = self.create_cook_to_test()
        dish = Dish.objects.create(
            name="dish_test",
            description="description dish test",
            price=10,
            dishtype=dishtype,
        )
        dish.cooks.add(cook)
        return dish

    def create_ingredient_to_test(self):
        dish = self.create_dish_to_test()
        ingredient = Ingredient.objects.create(
            name="ingredient_test",
        )
        ingredient.dishes.add(dish)
        return ingredient

    def test_dishtype_str(self):
        dishtype = self.create_dishtype_to_test()
        self.assertEqual(
            str(dishtype),
            dishtype.name
        )

    def test_dish_str(self):
        dish = self.create_dish_to_test()
        self.assertEqual(
            str(dish),
            dish.name
        )

    def test_create_cook_with_years_of_experience(self):
        username = "cook_test"
        password = "pass_cook_test"
        first_name = "Firstname_cook_test"
        last_name = "Lastname_cook_test"
        years_of_experience = 10
        cook = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            years_of_experience=years_of_experience,
        )
        self.assertEqual(cook.username, username)
        self.assertEqual(cook.first_name, first_name)
        self.assertEqual(cook.last_name, last_name)
        self.assertEqual(cook.years_of_experience, years_of_experience)
        self.assertTrue(cook.check_password(password))

    def test_get_absolute_url(self):
        cook = self.create_cook_to_test()
        expected_url = reverse("kitchen:cook-detail", kwargs={"pk": cook.pk})
        self.assertEqual(cook.get_absolute_url(), expected_url)
