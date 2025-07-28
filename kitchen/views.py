from http.client import HTTPResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from kitchen.forms import DishTypeCreationForm, DishCreationForm, IngredientCreationForm, CookCreationForm, \
    CookUpdateForm
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
    context_object_name = "dishtype_list"
    template_name = "kitchen/dishtype_list.html"
    paginate_by = 5

class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType
    template_name = "kitchen/dishtype_detail.html"
    queryset = DishType.objects.all().prefetch_related("dishes")


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    form_class = DishTypeCreationForm
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    form_class = DishTypeCreationForm
    success_url = reverse_lazy("kitchen:dish-type-detail")

    def get_success_url(self):
        return reverse("kitchen:dish-type-detail", kwargs={"pk": self.object.id})


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    context_object_name = "dish_list"
    template_name = "kitchen/dish_list.html"
    paginate_by = 5
    queryset = Dish.objects.all().select_related("dishtype")


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    queryset = Dish.objects.all().prefetch_related("cooks", "ingredients")


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishCreationForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishCreationForm
    success_url = reverse_lazy("kitchen:dish-detail")

    def get_success_url(self):
        return reverse("kitchen:dish-detail", kwargs={"pk": self.object.id})


class DishAddCookView(LoginRequiredMixin, generic.DetailView):
    model = Dish

    def post(self, request, pk):
        dish = self.get_object()
        dish.cooks.add(request.user)
        dish.save()
        return HttpResponseRedirect(reverse("kitchen:dish-detail", args=[pk]))



class DishRemoveCookView(LoginRequiredMixin, generic.DetailView):
    model = Dish

    def post(self, request, pk):
        dish = self.get_object()
        dish.cooks.remove(request.user)
        dish.save()
        return HttpResponseRedirect(reverse("kitchen:dish-detail", args=[pk]))


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    context_object_name = "ingredient_list"
    template_name = "kitchen/ingredient_list.html"
    paginate_by = 5


class IngredientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ingredient
    queryset = Ingredient.objects.all().prefetch_related("dishes")


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    form_class = IngredientCreationForm
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    form_class = IngredientCreationForm
    success_url = reverse_lazy("kitchen:ingredient-detail")

    def get_success_url(self):
        return reverse("kitchen:ingredient-detail", kwargs={"pk": self.object.id})


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    success_url = reverse_lazy("kitchen:ingredient-list")


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    context_object_name = "cook_list"
    template_name = "kitchen/cook_list.html"
    paginate_by = 5


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    reverse_lazy = reverse_lazy("kitchen:cook-list")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookUpdateForm
    success_url = reverse_lazy("kitchen:cook-detail")

    def get_success_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.object.id})


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")
