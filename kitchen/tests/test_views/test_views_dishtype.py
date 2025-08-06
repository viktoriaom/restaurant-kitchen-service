from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from django.urls import reverse

from kitchen.models import DishType

DISHTYPE_LIST_URL = reverse("kitchen:dish-type-list")
pagination_num = 5


class PublicDishtypeTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DISHTYPE_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDishtypeTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="cook",
            password="cook_test",
        )
        group = Group.objects.get(name="manager")
        self.user.groups.add(group)
        self.client.force_login(self.user)

    def create_dishtypes_for_test(self):
        DishType.objects.create(
            name="Snacks"
        )
        DishType.objects.create(
            name="Mains"
        )
        for num in range(pagination_num * 2):
            DishType.objects.create(
                name=f"Dishtypetest {num}"
            )

    def test_retrieve_dishtypes(self):
        self.create_dishtypes_for_test()
        response = self.client.get(DISHTYPE_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cars = DishType.objects.all()
        self.assertEqual(
            list(response.context["dishtype_list"]),
            list(cars[:pagination_num])
        )
        self.assertTemplateUsed(response, "kitchen/dishtype_list.html")
        search_response = self.client.get(f"{DISHTYPE_LIST_URL}?name=m")
        self.assertContains(search_response, "Mains")
        self.assertNotContains(search_response, "Snacks")

    def test_dishtype_pagination(self):
        self.create_dishtypes_for_test()
        response = self.client.get(DISHTYPE_LIST_URL)
        self.assertEqual(len(response.context["dishtype_list"]),
                         pagination_num)

    def test_dishtype_detail(self):
        self.create_dishtypes_for_test()
        dishtype = DishType.objects.get(id=1)
        response = self.client.get(reverse(
            "kitchen:dish-type-detail", args=[dishtype.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dishtype_detail.html")
        self.assertEqual(response.context["dishtype"], dishtype)
        self.assertContains(response, f"{dishtype.name}")
        response = self.client.get(reverse(
            "kitchen:dish-type-detail", args=[9999])
        )
        self.assertEqual(response.status_code, 404)

    def test_create_dishtype(self):
        form_data = {
            "name": "test_dishtype",
        }
        self.client.post(reverse("kitchen:dish-type-create"), data=form_data)
        new_dishtype = DishType.objects.get(name=form_data["name"])

        self.assertEqual(
            new_dishtype.name, form_data["name"]
        )

    def test_update_dishtype(self):
        dishtype = DishType.objects.create(
            name="dishtype_test")

        update_data = {
            "name": "updated_dishtype"
        }
        response = self.client.post(reverse(
            "kitchen:dish-type-update", args=[dishtype.id]), data=update_data
        )
        dishtype.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            "kitchen:dish-type-detail", kwargs={"pk": dishtype.id})
                             )

        self.assertEqual(
            dishtype.name, "updated_dishtype"
        )

    def test_delete_dishtype(self):
        new_dishtype = DishType.objects.create(
            name="dishtype_test")
        response = self.client.post(
            reverse("kitchen:dish-type-delete", args=[new_dishtype.id])
        )
        self.assertRedirects(response, reverse("kitchen:dish-type-list"))
        self.assertFalse(DishType.objects.filter(
            pk=new_dishtype.id).exists()
                         )
