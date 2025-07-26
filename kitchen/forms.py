from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from kitchen.models import DishType, Dish, Ingredient, Cook


class DishTypeCreationForm(forms.ModelForm):
    class Meta:
        model = DishType
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control ", "placeholder": "Dish type name"}
            ),
        }


class DishCreationForm(forms.ModelForm):

    class Meta:
        model = Dish
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control ", "placeholder": "Dish name"}
            ),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "dishtype": forms.Select(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.5"}),
            "cooks": forms.CheckboxSelectMultiple(attrs={"class": "form-checkbox"}),
        }


class IngredientCreationForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control ", "placeholder": "Ingredient name"}
            ),
            "dishes": forms.CheckboxSelectMultiple(attrs={"class": "form-checkbox"}),
        }


class CookCreationForm(UserCreationForm):
    class Meta:
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control ", "placeholder": "Username"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control ", "placeholder": "First name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control ", "placeholder": "Last name"}
            ),
            "years_of_experience": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Years of experience"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Password"
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm password"
        })


class CookUpdateForm(LoginRequiredMixin, forms.ModelForm):
    class Meta:
        model = Cook
        fields = [
            "username",
            "first_name",
            "last_name",
            "years_of_experience",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control ", "placeholder": "Username"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control ", "placeholder": "First name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control ", "placeholder": "Last name"}
            ),
            "years_of_experience": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Years of experience"}),
        }
