from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from django.urls import reverse
from kitchen.models import DishType, Dish, Ingredient

DISH_LIST_URL = reverse("kitchen:dish-list")
pagination_num = 5


class PublicDishTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DISH_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDishTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="cook",
            password="cook_test",
        )
        group = Group.objects.get(name="manager")
        self.user.groups.add(group)
        self.client.force_login(self.user)

    def create_dishes_for_test(self):
        dishtype = DishType.objects.create(
            name="DishType_test",
        )
        cook = get_user_model().objects.create_user(
            username="cook_test",
            password="pass_cook_test",
            first_name="Firstname_cook_test",
            last_name="Lastname_cook_test",
            years_of_experience=10,
        )
        cook_additional = get_user_model().objects.create_user(
            username="cook_additional",
            password="pass_cook_additional_test",
            first_name="Firstname_cook_additional_test",
            last_name="Lastname_cook_additional_test",
            years_of_experience=100,
        )

        dish_one = Dish.objects.create(
            name="Olives",
            description="description dish test",
            price=10,
            dishtype=dishtype,
        )
        dish_one.cooks.add(cook)
        dish_one.cooks.add(cook_additional)
        ingredient_one = Ingredient.objects.create(
            name="Ingredient_one_test",
        )
        ingredient_one.dishes.add(dish_one)
        ingredient_two = Ingredient.objects.create(
            name="Ingredient_two_test",
        )
        ingredient_two.dishes.add(dish_one)
        dish_two = Dish.objects.create(
            name="Bread and butter",
            description="description dish test",
            price=10,
            dishtype=dishtype,
        )
        dish_two.cooks.add(cook)
        for num in range(pagination_num * 2):
            dish = Dish.objects.create(
                name=f"Dishtest {num}",
                description="description dish test",
                price=10,
                dishtype=dishtype
            )
            dish.cooks.add(cook)

    def test_retrieve_dishes(self):
        self.create_dishes_for_test()
        response = self.client.get(DISH_LIST_URL)
        self.assertEqual(response.status_code, 200)
        dishes = Dish.objects.all()
        self.assertEqual(
            list(response.context["dish_list"]),
            list(dishes[:pagination_num])
        )
        dishes = response.context["dish_list"]
        for dish in dishes:
            self.assertContains(response, dish.name)
            self.assertContains(response, dish.price)
            self.assertContains(response, dish.dishtype.name)

        self.assertTemplateUsed(response, "kitchen/dish_list.html")
        search_response = self.client.get(f"{DISH_LIST_URL}?name=br")
        self.assertContains(search_response, "Bread and butter")
        self.assertNotContains(search_response, "Olives")

    def test_dish_pagination(self):
        self.create_dishes_for_test()
        response = self.client.get(DISH_LIST_URL)
        self.assertEqual(len(response.context["dish_list"]), pagination_num)

    def test_dish_detail(self):
        self.create_dishes_for_test()
        dish = Dish.objects.get(id=1)
        response = self.client.get(reverse(
            "kitchen:dish-detail", args=[dish.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                "kitchen/dish_detail.html"
                                )
        self.assertEqual(response.context["dish"], dish)
        self.assertContains(response, f"{dish.name}")
        self.assertContains(response, f"{dish.description}")
        self.assertContains(response, f"{dish.price}")

        for cook in dish.cooks.all():
            self.assertContains(response, cook.username)

        for ingredient in dish.ingredients.all():
            self.assertContains(response, ingredient.name)

        response = self.client.get(reverse("kitchen:dish-detail", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_create_dish(self):
        dishtype = DishType.objects.create(
            name="DishType_test",
        )
        cook = get_user_model().objects.get(id=1)
        form_data = {
            "name": "test_ingredient",
            "description": "description ingredient test",
            "price": 10,
            "dishtype": dishtype.id,
            "cooks": [cook.id],
        }
        response = self.client.post(reverse(
            "kitchen:dish-create"), data=form_data
        )
        new_dish = Dish.objects.get(name=form_data["name"])
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            new_dish.name, form_data["name"]
        )
        self.assertEqual(
            new_dish.description, form_data["description"]
        )
        self.assertEqual(
            new_dish.price, form_data["price"]
        )
        self.assertEqual(
            new_dish.dishtype, dishtype
        )

    def test_update_dish(self):
        dishtype = DishType.objects.create(
            name="DishType_test",
        )
        cook = get_user_model().objects.get(id=1)
        dish = Dish.objects.create(
            name="Dish one",
            description="description dish test",
            price=10,
            dishtype=dishtype,
        )

        update_data = {
            "name": "updated_dish_name",
            "description": "updated_description ingredient test",
            "price": 10,
            "dishtype": dishtype.id,
            "cooks": [cook.id],
        }
        response = self.client.post(reverse(
            "kitchen:dish-update", args=[dish.id]), data=update_data
        )
        dish.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            "kitchen:dish-detail", kwargs={"pk": dish.id})
                             )
        self.assertEqual(
            dish.name, "updated_dish_name"
        )
        self.assertEqual(
            dish.description, "updated_description ingredient test"
        )

    def test_delete_dish(self):
        dishtype = DishType.objects.create(
            name="DishType_test",
        )
        cook = get_user_model().objects.get(id=1)
        dish = Dish.objects.create(
            name="Pasta",
            description="description dish test",
            price=10,
            dishtype=dishtype,
        )
        dish.cooks.add(cook)

        response = self.client.post(
            reverse("kitchen:dish-delete", args=[dish.id])
        )
        self.assertRedirects(response, reverse("kitchen:dish-list"))
        self.assertFalse(Dish.objects.filter(
            pk=dish.id).exists()
                         )

    def test_dish_update_ingredient(self):
        dishtype = DishType.objects.create(
            name="DishType_test",
        )
        cook = get_user_model().objects.get(id=1)
        dish = Dish.objects.create(
            name="Pasta",
            description="description dish test",
            price=10,
            dishtype=dishtype,
        )
        dish.cooks.add(cook)
        ingredient_one = Ingredient.objects.create(
            name="Ingredient_one_test",
        )
        ingredient_two = Ingredient.objects.create(
            name="Ingredient_two_test",
        )
        ingredient_one.dishes.add(dish)

        response = self.client.get(
            reverse("kitchen:dish-update-ingredient", args=[dish.id])
        )
        self.assertContains(response, ingredient_one.name)
        self.assertContains(response, ingredient_two.name)
        dish_ingredients = dish.ingredients.all()
        self.assertIn(ingredient_one, dish_ingredients)
        self.assertNotIn(ingredient_two, dish_ingredients)
        self.assertTemplateUsed(
            response, "kitchen/dish_update_ingredient.html"
        )
        response = self.client.post(
            reverse("kitchen:dish-update-ingredient", args=[dish.id]),
            data={"ingredient_id": ingredient_two.id, "action": "add"}
        )
        self.assertEqual(response.status_code, 302)
        dish_ingredients = dish.ingredients.all()
        self.assertIn(ingredient_one, dish_ingredients)
        self.assertIn(ingredient_two, dish_ingredients)
        response = self.client.post(
            reverse("kitchen:dish-update-ingredient", args=[dish.id]),
            data={"ingredient_id": ingredient_one.id, "action": "remove"}
        )
        self.assertEqual(response.status_code, 302)
        dish_ingredients = dish.ingredients.all()
        self.assertNotIn(ingredient_one, dish_ingredients)
        self.assertIn(ingredient_two, dish_ingredients)

    def test_dish_update_ingredient_pagination(self):
        dishtype = DishType.objects.create(
            name="DishType_test",
        )
        dish = Dish.objects.create(
            name="Pasta",
            description="description dish test",
            price=10,
            dishtype=dishtype,
        )
        for num in range(pagination_num * 2):
            ingredient = Ingredient.objects.create(
                name=f"Ingredient_test {num}",
            )
            ingredient.dishes.add(dish)

        response = self.client.get(reverse(
            "kitchen:dish-update-ingredient", args=[dish.id])
        )
        self.assertEqual(
            len(response.context["ingredient_list"]), pagination_num
        )
