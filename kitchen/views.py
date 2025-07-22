from django.shortcuts import render
from django.views import generic

from kitchen.models import Cook, Dish, Ingredient, DishType


# Create your views here.
def index(request):
    num_cooks = Cook.objects.all().count()
    num_dishes = Dish.objects.all().count()
    num_categories = DishType.objects.all().count()
    num_ingredients = Ingredient.objects.all().count()

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_categories": num_categories,
        "num_ingredients": num_ingredients,
    }

    return render(request, "kitchen/index.html", context=context)

class DishTypeListView(generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 5

class DishTypeDetailView(generic.DetailView):
    model = DishType
    template_name = "kitchen/dish_type_detail.html"
    queryset = DishType.objects.all().prefetch_related("dishes")

class DishListView(generic.ListView):
    model = Dish
    context_object_name = "dish_list"
    template_name = "kitchen/dish_list.html"
    paginate_by = 5
    queryset = Dish.objects.all().select_related("dish_type")


class DishDetailView(generic.DetailView):
    model = Dish
    queryset = Dish.objects.all().prefetch_related("cooks", "ingredients")


class IngredientListView(generic.ListView):
    model = Ingredient
    context_object_name = "ingredient_list"
    template_name = "kitchen/ingredient_list.html"
    paginate_by = 5


class IngredientDetailView(generic.DetailView):
    model = Ingredient
    queryset = Ingredient.objects.all().prefetch_related("dishes")


class CookListView(generic.ListView):
    model = Cook
    context_object_name = "cook_list"
    template_name = "kitchen/cook_list.html"
    paginate_by = 5


class CookDetailView(generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes")
