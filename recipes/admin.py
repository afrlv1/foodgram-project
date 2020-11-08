from django.contrib import admin

from .models import (
    Recipe,
    RecipeIngredient,
    Ingredient,
    FollowRecipe,
    FollowUser,
    ShoppingList,
)


# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    # показывает сколько раз рецепт добавлен в избранное
    readonly_fields = ("favorite_amount",)

    list_display = ("name", "author")
    search_fields = ("name", "author__username")
    list_filter = ("author", "tags")


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("title", "dimension")
    search_fields = ("title",)
    empty_value_display = "-пусто-"


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(FollowRecipe)
admin.site.register(FollowUser)
admin.site.register(ShoppingList)
