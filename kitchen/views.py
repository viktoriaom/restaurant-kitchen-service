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


class DishListView(generic.ListView):
    model = Dish
    context_object_name = "dish_list"
    template_name = "kitchen/dish_list.html"


