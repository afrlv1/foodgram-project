import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from recipes.models import FollowRecipe, Recipe, FollowUser, ShoppingList
from users.forms import User


class GenericView(LoginRequiredMixin, View):
    def post(self, request, klass, *args, **kwargs):
        req_ = json.loads(request.body)
        queryset_id = req_.get("id", None)
        if queryset_id is not None:
            queryset = get_object_or_404(Recipe, id=recipe_id)
            obj, created = FollowRecipe.objects.get_or_create(user=request.user, recipe=queryset)
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        queryset = get_object_or_404(FollowRecipe, recipe=recipe_id, user=request.user)
        queryset.delete()
        return JsonResponse({"success": True})


class Ingredients(LoginRequiredMixin, View):
    """
    Получение ингредиентов для создания/редактирования рецепвта
    """

    def get(self, request):
        query = request.GET.get("query", None)
        if query is not None:
            response = Ingredients.objects.filter(title__icontains=query).values(
                "title", "dimension"
            )
            return JsonResponse(list(response), safe=False)
        return JsonResponse({"success": False}, status=400)


class Favorites(LoginRequiredMixin, View):
    """
    Добавление/удаление рецепта из "Избранное"
    """

    def post(self, request):
        req_ = json.loads(request.body)
        recipe_id = req_.get("id", None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            obj, created = FollowRecipe.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(FollowRecipe, recipe=recipe_id, user=request.user)
        recipe.delete()
        return JsonResponse({"success": True})


class Subscribe(LoginRequiredMixin, View):
    """
    Добавление/удаления автора в "Мои подписки"
    """

    def post(self, request):
        req_ = json.loads(request.body)
        user_id = req_.get("id", None)
        if user_id is not None:
            if self.request.user.id == user_id:
                return JsonResponse({"success": False}, status=403)
            author = get_object_or_404(User, pk=user_id)
            obj, created = FollowUser.objects.get_or_create(
                user=request.user, author=author
            )
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, author_id):
        following = get_object_or_404(FollowUser, user=request.user, author=author_id)
        following.delete()
        return JsonResponse({"success": True})


class Purchase(LoginRequiredMixin, View):
    """
    Добавить/ удалить рецепты из списка покупок
    """

    def post(self, request):
        req_ = json.loads(request.body)
        recipe_id = req_.get("id", None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            obj, created = ShoppingList.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        card_obj = get_object_or_404(
            ShoppingList, user=request.user, recipe_id=recipe_id
        )
        card_obj.delete()
        return JsonResponse({"success": True})
