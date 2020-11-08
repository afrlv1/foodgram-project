from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)
    color = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    dimension = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    description = models.TextField()
    cooking_time = models.IntegerField(default=0)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    tags = models.ManyToManyField(Tag, related_name="recipes")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def favorite_amount(self):
        return self.recipe_followers.count()

    @property
    def description_as_list(self):
        return self.description.split("\n")


class FollowRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following_recipes"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe_followers"
    )

    def __str__(self):
        return f"User: {self.user} Follow:{self.recipe}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe_ingredients"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="recipes"
    )
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.ingredient.title} - {self.amount} ({self.ingredient.dimension})"


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_shopping_list"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="shopping_list"
    )

    def __str__(self):
        return f"User: {self.user} Recipe: {self.recipe}"


class FollowUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f"User: {self.user} Follow: {self.author}"


def is_following(self, user):
    """
    Поиск юзера в текущих подписчиках пользователя
    """
    return self.following.filter(user=user).exists()


User.add_to_class("is_following", is_following)
