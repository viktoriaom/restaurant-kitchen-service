from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import GroupRequiredMixin

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic


from kitchen.forms import (
    DishTypeCreationForm,
    DishCreationForm,
    IngredientCreationForm,
    CookCreationForm,
    CookUpdateForm,
    CookSearchForm,
    IngredientSearchForm,
    DishSearchForm,
    DishTypeSearchForm)

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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        name = self.request.GET.get("name")
        if name:
            return DishType.objects.filter(name__icontains=name)
        return DishType.objects.all()


class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType
    template_name = "kitchen/dishtype_detail.html"
    queryset = DishType.objects.all().prefetch_related("dishes")


class DishTypeCreateView(GroupRequiredMixin,
                         LoginRequiredMixin,
                         generic.CreateView):
    group_required = ["employee", "manager"]
    model = DishType
    form_class = DishTypeCreationForm
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeUpdateView(GroupRequiredMixin,
                         LoginRequiredMixin,
                         generic.UpdateView):
    group_required = ["employee", "manager"]
    model = DishType
    form_class = DishTypeCreationForm
    success_url = reverse_lazy("kitchen:dish-type-detail")

    def get_success_url(self):
        return reverse(
            "kitchen:dish-type-detail", kwargs={"pk": self.object.id}
        )


class DishTypeDeleteView(GroupRequiredMixin,
                         LoginRequiredMixin,
                         generic.DeleteView):
    group_required = ["employee", "manager"]
    model = DishType
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    context_object_name = "dish_list"
    template_name = "kitchen/dish_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        name = self.request.GET.get("name")
        if name:
            return Dish.objects.filter(
                name__icontains=name).select_related("dishtype")
        return Dish.objects.all().select_related("dishtype")


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    queryset = Dish.objects.all().prefetch_related("cooks", "ingredients")


class DishCreateView(GroupRequiredMixin,
                     LoginRequiredMixin,
                     generic.CreateView):
    group_required = ["employee", "manager"]
    model = Dish
    form_class = DishCreationForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(GroupRequiredMixin,
                     LoginRequiredMixin,
                     generic.UpdateView):
    group_required = ["employee", "manager"]
    model = Dish
    form_class = DishCreationForm
    success_url = reverse_lazy("kitchen:dish-detail")

    def get_success_url(self):
        return reverse("kitchen:dish-detail", kwargs={"pk": self.object.id})


class DishAddCookView(GroupRequiredMixin,
                      LoginRequiredMixin,
                      generic.DetailView):
    group_required = ["employee", "manager"]
    model = Dish

    def post(self, request, pk):
        dish = self.get_object()
        dish.cooks.add(request.user)
        dish.save()
        return HttpResponseRedirect(reverse("kitchen:dish-detail", args=[pk]))


class DishRemoveCookView(GroupRequiredMixin,
                         LoginRequiredMixin,
                         generic.DetailView):
    group_required = ["employee", "manager"]
    model = Dish

    def post(self, request, pk):
        dish = self.get_object()
        dish.cooks.remove(request.user)
        dish.save()
        return HttpResponseRedirect(reverse("kitchen:dish-detail", args=[pk]))


class DishUpdateIngredientView(GroupRequiredMixin,
                               LoginRequiredMixin,
                               generic.ListView):
    group_required = ["employee", "manager"]
    model = Ingredient
    template_name = "kitchen/dish_update_ingredient.html"
    paginate_by = 5

    def get_queryset(self):
        name = self.request.GET.get("name")
        if name:
            return Ingredient.objects.filter(name__icontains=name)
        return Ingredient.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dish"] = get_object_or_404(Dish, pk=self.kwargs["pk"])
        name = self.request.GET.get("name", "")
        context["search_form"] = IngredientSearchForm(
            initial={"name": name}
        )
        return context

    def post(self, request, pk):
        dish = get_object_or_404(Dish, pk=pk)
        ingredient_pk = request.POST.get("ingredient_id")
        action = request.POST.get("action")
        ingredient = get_object_or_404(Ingredient, pk=ingredient_pk)

        if action == "add":
            dish.ingredients.add(ingredient)
        elif action == "remove":
            dish.ingredients.remove(ingredient)

        return redirect(reverse(
            "kitchen:dish-update-ingredient", kwargs={"pk": pk})
        )


class DishDeleteView(GroupRequiredMixin,
                     LoginRequiredMixin,
                     generic.DeleteView):
    group_required = ["employee", "manager"]
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    context_object_name = "ingredient_list"
    template_name = "kitchen/ingredient_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IngredientListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = IngredientSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        name = self.request.GET.get("name")
        if name:
            return Ingredient.objects.filter(name__icontains=name)
        return Ingredient.objects.all()


class IngredientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ingredient
    queryset = Ingredient.objects.all().prefetch_related("dishes")


class IngredientCreateView(GroupRequiredMixin,
                           LoginRequiredMixin,
                           generic.CreateView):
    group_required = ["employee", "manager"]
    model = Ingredient
    form_class = IngredientCreationForm
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientUpdateView(GroupRequiredMixin,
                           LoginRequiredMixin,
                           generic.UpdateView):
    group_required = ["employee", "manager"]
    model = Ingredient
    form_class = IngredientCreationForm
    success_url = reverse_lazy("kitchen:ingredient-detail")

    def get_success_url(self):
        return reverse(
            "kitchen:ingredient-detail", kwargs={"pk": self.object.id}
        )


class IngredientDeleteView(GroupRequiredMixin,
                           LoginRequiredMixin,
                           generic.DeleteView):
    group_required = ["employee", "manager",]
    model = Ingredient
    success_url = reverse_lazy("kitchen:ingredient-list")


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    context_object_name = "cook_list"
    template_name = "kitchen/cook_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CookSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        username = self.request.GET.get("username")
        if username:
            return Cook.objects.filter(username__icontains=username)
        return Cook.objects.all()


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cook = self.object
        try:
            cook_group = cook.groups.first()  # Assuming one group per cook
        except Exception:
            cook_group = None
        context["cook_group"] = cook_group
        return context


class CookCreateView(GroupRequiredMixin,
                     LoginRequiredMixin,
                     generic.CreateView):
    group_required = ["manager"]
    model = Cook
    form_class = CookCreationForm
    reverse_lazy = reverse_lazy("kitchen:cook-list")


class CookUpdateView(GroupRequiredMixin,
                     LoginRequiredMixin,
                     generic.UpdateView):
    group_required = ["manager"]
    model = Cook
    form_class = CookUpdateForm
    success_url = reverse_lazy("kitchen:cook-detail")

    def get_success_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.object.id})


class CookDeleteView(GroupRequiredMixin,
                     LoginRequiredMixin,
                     generic.DeleteView):
    group_required = ["manager"]
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")
