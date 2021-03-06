import datetime as dt
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecipesForm
from .models import Recipe, Ingredients, FollowUser, ShoppingList, RecipeIngredient, Tag
from .utils import get_ingredients


def index(request):
    tags_filter = request.GET.getlist("filters")
    recipe_list = Recipe.objects.order_by("-pub_date").all()
    if tags_filter:
        recipe_list = recipe_list.filter(tags__slug__in=tags_filter).distinct().all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "indexAuth.html",
        {
            "page": page,
            "paginator": paginator,
        },
    )


def new_recipe(request):
    user = User.objects.get(username=request.user)
    if request.method == "POST":
        form = RecipesForm(request.POST or None, files=request.FILES or None)
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, "Добавьте ингредиенты")
        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = user
            recipe.save()
            for ing_name, amount in ingredients.items():
                ingredient = get_object_or_404(Ingredients, title=ing_name)
                recipe_ing = RecipeIngredient(
                    recipe=recipe, ingredient=ingredient, amount=amount
                )
                recipe_ing.save()
            form.save_m2m()
            return redirect("index")
    else:
        form = RecipesForm()
    return render(request, "formRecipe.html", {"form": form})


def recipe_view(request, recipe_id, username):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    username = get_object_or_404(User, username=username)
    return render(request, "singlePage.html", {"username": username, "recipe": recipe})


def profile(request, username):
    username = get_object_or_404(User, username=username)
    tag = request.GET.getlist("filters")
    recipes = Recipe.objects.filter(author=username).order_by("-pub_date").all()
    if tag:
        recipes = recipes.filter(tags__slug__in=tag)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "authorRecipe.html",
        {
            "username": username,
            "page": page,
            "paginator": paginator,
        },
    )


def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect("index")
    if request.method == "POST":
        form = RecipesForm(
            request.POST or None, files=request.FILES or None, instance=recipe
        )
        ingredients = get_ingredients(request)
        if form.is_valid():
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for item in ingredients:
                RecipeIngredient.objects.create(
                    ingredient=Ingredients.objects.get(title=f"{item}"),
                    recipe=recipe,
                )
            form.save_m2m()
        return redirect("index")
    form = RecipesForm(request.POST or None, files=request.FILES or None, instance=recipe)
    return render(
        request,
        "recipe_edit.html",
        {"form": form, "recipe": recipe},
    )


def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
    return redirect("index")


def favorite(request):
    tags_filter = request.GET.getlist("filters")
    recipe_list = Recipe.objects.filter(follow_recipe__user__id=request.user.id).all()
    if tags_filter:
        recipe_list = recipe_list.filter(tags__slug__in=tags_filter).distinct().all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "favorite.html",
        {"page": page, "paginator": paginator},
    )


def follow(request):
    author_list = FollowUser.objects.filter(user__id=request.user.id).all()
    paginator = Paginator(author_list, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "myFollow.html",
        {"page": page, "paginator": paginator, "author": author_list},
    )


def shopping_list(request):
    if request.user.is_active:
        shop_list = ShoppingList.objects.filter(user=request.user).all()
        return render(request, "shopList.html", {"shop_list": shop_list})
    else:
        shop_list = ShoppingList.objects.first()
        return render(request, "shopList.html", {"shop_list": shop_list})


def download_card(request):
    recipes = Recipe.objects.filter(recipe_shopping_list__user=request.user)
    ingredients = recipes.values(
        "ingredients__title", "ingredients__dimension"
    ).annotate(total_amount=Sum("recipe_ingredients__amount"))
    file_data = ""
    for item in ingredients:
        line = " ".join(str(value) for value in item.values())
        file_data += line + "\n"
    response = HttpResponse(file_data, content_type="application/text charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="ShoppingList.txt"'
    return response


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
