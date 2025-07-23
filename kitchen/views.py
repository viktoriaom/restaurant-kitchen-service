from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from kitchen.models import Cook, Dish, Ingredient, DishType


# Create your views here.
@login_required
def index(request):
    num_cooks = Cook.objects.all().count()
    num_dishes = Dish.objects.all().count()
    num_dishtypes = DishType.objects.all().count()
    num_ingredients = Ingredient.objects.all().count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dishtypes": num_dishtypes,
        "num_ingredients": num_ingredients,
        "num_visits": num_visits,
    }

    return render(request, "kitchen/index.html", context=context)

class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 5

class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType
    template_name = "kitchen/dish_type_detail.html"
    queryset = DishType.objects.all().prefetch_related("dishes")

class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    context_object_name = "dish_list"
    template_name = "kitchen/dish_list.html"
    paginate_by = 5
    queryset = Dish.objects.all().select_related("dish_type")


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    queryset = Dish.objects.all().prefetch_related("cooks", "ingredients")


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    context_object_name = "ingredient_list"
    template_name = "kitchen/ingredient_list.html"
    paginate_by = 5


class IngredientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ingredient
    queryset = Ingredient.objects.all().prefetch_related("dishes")


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    context_object_name = "cook_list"
    template_name = "kitchen/cook_list.html"
    paginate_by = 5


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes")
