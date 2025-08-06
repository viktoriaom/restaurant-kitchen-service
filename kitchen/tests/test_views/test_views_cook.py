from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from django.urls import reverse
from kitchen.models import DishType, Dish, Cook

COOK_LIST_URL = reverse("kitchen:cook-list")
pagination_num = 5


class PublicCookTest(TestCase):
    def test_login_required(self):
        response = self.client.get(COOK_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCookTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="cook",
            password="cook_test",
        )
        group = Group.objects.get(name="manager")
        self.user.groups.add(group)
        self.client.force_login(self.user)

    def create_cooks_for_test(self):
        dishtype = DishType.objects.create(
            name="DishType_test",
        )
        cook_first = get_user_model().objects.create_user(
            username="first_cook_test",
            password="pass_cook_test",
            first_name="Firstname_cook_test",
            last_name="Lastname_cook_test",
            years_of_experience=10,
        )
        cook_second = get_user_model().objects.create_user(
            username="second_cook_test",
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
        dish_two = Dish.objects.create(
            name="Bread and butter",
            description="description dish test",
            price=10,
            dishtype=dishtype,
        )

        dish_one.cooks.add(cook_first)
        dish_one.cooks.add(cook_second)
        dish_two.cooks.add(cook_first)

        for num in range(pagination_num * 2):
            Cook.objects.create(
                username=f"cook_{num}",
                password=f"pass_cook_test{num}",
                first_name=f"Firstname_cook_{num}",
                last_name=f"Lastname_cook_{num}",
                years_of_experience=num,
            )

    def test_retrieve_cooks(self):
        self.create_cooks_for_test()
        response = self.client.get(COOK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        users = list(Cook.objects.all())
        self.assertEqual(
            list(response.context["cook_list"]),
            list(users[:pagination_num])
        )
        cooks = response.context["cook_list"]
        for cook in cooks:
            self.assertContains(response, cook.username)
            self.assertContains(response, cook.first_name)
            self.assertContains(response, cook.last_name)
            self.assertContains(response, cook.years_of_experience)

        self.assertTemplateUsed(response, "kitchen/cook_list.html")
        search_response = self.client.get(f"{COOK_LIST_URL}?username=fi")
        self.assertContains(search_response, "first_cook_test")
        self.assertNotContains(search_response, "second_cook_test")

    def test_cook_pagination(self):
        self.create_cooks_for_test()
        response = self.client.get(COOK_LIST_URL)
        self.assertEqual(len(response.context["cook_list"]), pagination_num)

    def test_cook_detail(self):
        self.create_cooks_for_test()
        cook = Cook.objects.get(id=2)
        response = self.client.get(reverse(
            "kitchen:cook-detail", args=[cook.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                "kitchen/cook_detail.html"
                                )
        self.assertEqual(response.context["cook"], cook)
        self.assertContains(response, cook.username)
        self.assertContains(response, cook.first_name)
        self.assertContains(response, cook.last_name)
        self.assertContains(response, cook.years_of_experience)

        for dish in cook.dishes.all():
            self.assertContains(response, dish.name)

        response = self.client.get(reverse("kitchen:cook-detail", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_create_cook(self):
        form_data = {
            "username": "test_username",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test First",
            "last_name": "Test Last",
            "years_of_experience": 2354,
        }
        self.client.post(reverse("kitchen:cook-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(
            new_user.first_name, form_data["first_name"]
        )
        self.assertEqual(
            new_user.last_name, form_data["last_name"]
        )
        self.assertEqual(
            new_user.years_of_experience, form_data["years_of_experience"]
        )

    def test_update_cook(self):
        cook_new = get_user_model().objects.create_user(
            username="cook_test",
            password="pass_cook_test",
            first_name="Firstname_cook_test",
            last_name="Lastname_cook_test",
            years_of_experience=10,
        )

        update_data = {
            "username": "cook_test",
            "first_name": "Updated First name",
            "last_name": "Lastname_cook_test",
            "years_of_experience": 2354,
        }
        response = self.client.post(reverse(
            "kitchen:cook-update", args=[cook_new.id]), data=update_data
        )
        cook_new.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            "kitchen:cook-detail", kwargs={"pk": cook_new.id})
                             )

        self.assertEqual(
            cook_new.first_name, "Updated First name"
        )
        self.assertEqual(
            cook_new.years_of_experience, 2354
        )

    def test_delete_cook(self):
        cook_new = get_user_model().objects.create_user(
            username="cook_test",
            password="pass_cook_test",
            first_name="Firstname_cook_test",
            last_name="Lastname_cook_test",
            years_of_experience=10,
        )
        response = self.client.post(
            reverse("kitchen:cook-delete", args=[cook_new.id])
        )
        self.assertRedirects(response, reverse("kitchen:cook-list"))
        self.assertFalse(get_user_model().objects.filter(
            pk=cook_new.id).exists()
                         )
