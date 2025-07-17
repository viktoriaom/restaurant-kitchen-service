from django.shortcuts import render

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
