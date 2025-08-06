from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from django.urls import reverse
from kitchen.models import DishType, Dish, Ingredient

INGREDIENT_LIST_URL = reverse("kitchen:ingredient-list")
pagination_num = 5


class PublicIngredientTest(TestCase):
    def test_login_required(self):
        response = self.client.get(INGREDIENT_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateIngredientTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="cook",
            password="cook_test",
        )
        group = Group.objects.get(name="manager")
        self.user.groups.add(group)
        self.client.force_login(self.user)

    def create_ingredients_for_test(self):
        dishtype = DishType.objects.create(
            name="DishType_test",
        )
        dish = Dish.objects.create(
            name="Pasta",
            description="description dish test",
            price=10,
            dishtype=dishtype,
        )
        ingredient_one = Ingredient.objects.create(
            name="Cheese",
        )
        ingredient_one.dishes.add(dish)
        ingredient_two = Ingredient.objects.create(
            name="Tomato",
        )
        ingredient_two.dishes.add(dish)

        for num in range(pagination_num * 2):
            ingredient = Ingredient.objects.create(
                name=f"Ingredient_test {num}",
            )
            ingredient.dishes.add(dish)

    def test_retrieve_ingredients(self):
        self.create_ingredients_for_test()
        response = self.client.get(INGREDIENT_LIST_URL)
        self.assertEqual(response.status_code, 200)
        ingredients = Ingredient.objects.all()
        self.assertEqual(
            list(response.context["ingredient_list"]),
            list(ingredients[:pagination_num])
        )
        ingredients = response.context["ingredient_list"]

        for ingredient in ingredients:
            self.assertContains(response, ingredient.name)

        self.assertTemplateUsed(response, "kitchen/ingredient_list.html")
        search_response = self.client.get(f"{INGREDIENT_LIST_URL}?name=to")
        self.assertContains(search_response, "Tomato")
        self.assertNotContains(search_response, "Cheese")

    def test_ingredient_pagination(self):
        self.create_ingredients_for_test()
        response = self.client.get(INGREDIENT_LIST_URL)
        self.assertEqual(len(response.context["ingredient_list"]),
                         pagination_num
                         )

    def test_ingredient_detail(self):
        self.create_ingredients_for_test()
        ingredient = Ingredient.objects.get(id=1)
        response = self.client.get(reverse(
            "kitchen:ingredient-detail", args=[ingredient.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                "kitchen/ingredient_detail.html"
                                )
        self.assertEqual(response.context["ingredient"], ingredient)
        self.assertContains(response, f"{ingredient.name}")

        for dish in ingredient.dishes.all():
            self.assertContains(response, dish.name)

        response = self.client.get(reverse(
            "kitchen:ingredient-detail", args=[9999])
        )
        self.assertEqual(response.status_code, 404)

    def test_create_ingredient(self):
        dishtype = DishType.objects.create(
            name="DishType_test",
        )
        dish = Dish.objects.create(
            name="test dish",
            description="description dish test",
            price=10,
            dishtype=dishtype,
        )

        form_data = {
            "name": "test_ingredient",
            "dishes": [dish.id],
        }
        response = self.client.post(reverse(
            "kitchen:ingredient-create"), data=form_data
        )
        new_ingredient = Ingredient.objects.get(name=form_data["name"])
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            new_ingredient.name, form_data["name"]
        )
        self.assertIn(
            dish, new_ingredient.dishes.all()
        )

    def test_update_ingredient(self):
        dishtype = DishType.objects.create(
            name="DishType_test",
        )
        dish_one = Dish.objects.create(
            name="Dish one",
            description="description dish test",
            price=10,
            dishtype=dishtype,
        )
        dish_two = Dish.objects.create(
            name="Dish two",
            description="description dish test",
            price=10,
            dishtype=dishtype,
        )
        ingredient = Ingredient.objects.create(
            name="Cheese",
        )
        ingredient.dishes.add(dish_one)

        update_data = {
            "name": "updated_ingredient",
            "dishes": [dish_one.id, dish_two.id],
        }
        response = self.client.post(reverse(
            "kitchen:ingredient-update",
            args=[ingredient.id]), data=update_data
        )
        ingredient.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            "kitchen:ingredient-detail", kwargs={"pk": ingredient.id})
                             )

        self.assertEqual(
            ingredient.name, "updated_ingredient"
        )
        self.assertIn(
            dish_one, ingredient.dishes.all()
        )
        self.assertIn(
            dish_two, ingredient.dishes.all()
        )

    def test_delete_ingredient(self):
        dishtype = DishType.objects.create(
            name="DishType_test",
        )
        dish = Dish.objects.create(
            name="Pasta",
            description="description dish test",
            price=10,
            dishtype=dishtype,
        )
        ingredient = Ingredient.objects.create(
            name="Cheese",
        )
        ingredient.dishes.add(dish)

        response = self.client.post(
            reverse("kitchen:ingredient-delete", args=[ingredient.id])
        )
        self.assertRedirects(response, reverse("kitchen:ingredient-list"))
        self.assertFalse(Ingredient.objects.filter(
            pk=ingredient.id).exists()
                         )
