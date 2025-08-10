from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group

from kitchen.models import DishType, Dish, Ingredient, Cook


class DishTypeCreationForm(forms.ModelForm):
    class Meta:
        model = DishType
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control ",
                       "placeholder": "Dish type name"}
            ),
        }


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control ", "placeholder": "Search by name"}
        )
    )


class DishCreationForm(forms.ModelForm):

    class Meta:
        model = Dish
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control ", "placeholder": "Dish name"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "dishtype": forms.Select(
                attrs={"class": "form-control"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.5"}
            ),
            "cooks": forms.CheckboxSelectMultiple(
                attrs={"class": "form-checkbox"}
            ),
        }


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control ",
                   "placeholder": "Search by name"}
        )
    )


class IngredientCreationForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control ",
                       "placeholder": "Ingredient name"}
            ),
            "dishes": forms.CheckboxSelectMultiple(
                attrs={"class": "form-checkbox"}
            ),
        }


class IngredientSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control ",
                   "placeholder": "Search by name"}
        )
    )


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
                attrs={"class": "form-control ",
                       "placeholder": "Username"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control ",
                       "placeholder": "First name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control ",
                       "placeholder": "Last name"}
            ),
            "years_of_experience": forms.NumberInput(
                attrs={"class": "form-control",
                       "placeholder": "Years of experience"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["group"] = forms.ModelChoiceField(
            queryset=Group.objects.all(),
            required=False,
            widget=forms.Select(attrs={"class": "form-control"})
        )

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Password"
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm password"
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            group = self.cleaned_data.get("group")
            if group:
                user.groups.add(group)
        return user


class CookUpdateForm(LoginRequiredMixin, forms.ModelForm):
    class Meta:
        model = Cook
        fields = [
            "username",
            "first_name",
            "last_name",
            "years_of_experience",
            "group"
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control ",
                       "placeholder": "Username"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control ",
                       "placeholder": "First name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control ",
                       "placeholder": "Last name"}
            ),
            "years_of_experience": forms.NumberInput(
                attrs={"class": "form-control",
                       "placeholder": "Years of experience"}
            )
        }

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            groups = self.instance.groups.all()
            self.fields["group"].initial = groups[0] if groups else None

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            group = self.cleaned_data.get("group")
            user.groups.clear()
            if group:
                user.groups.add(group)
        return user


class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control ",
                   "placeholder": "Search by username"}
        )
    )
