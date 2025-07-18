from django.urls import path

from kitchen.views import index, DishTypeListView, DishListView, IngredientListView, CookListView

urlpatterns = [
    path("", index, name="index"),
    path("dish-types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
]

app_name = "kitchen"
