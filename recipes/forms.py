from django.forms import ModelForm, CheckboxSelectMultiple, ModelChoiceField
from recipes.models import Recipe, Ingredients


class RecipesForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ("title", "image", "description", "tags", "cooking_time")
        widgets = {
            "tags": CheckboxSelectMultiple(),
        }
