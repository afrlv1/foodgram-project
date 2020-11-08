from django.urls import path

from . import views

urlpatterns = [
    path("new_recipe", views.RecipeCreateView.as_view(), name="new_recipe"),
    path("<username>/", views.ProfileView.as_view(), name="profile"),
    path("recipe/<int:pk>/", views.RecipeDetailView.as_view(), name="recipe_page"),
    path("recipe/<int:pk>/edit", views.RecipeEditView.as_view(), name="edit_recipe"),
    path("recipe/<int:pk>/delete/", views.RecipeDeleteView.as_view(), name="delete_recipe", ),
    path("favorite_recipes", views.FavoriteView.as_view(), name="favorite_recipes"),
    path("card", views.CardView.as_view(), name="card"),
    path("my_subscriptions", views.FollowView.as_view(), name="my_subscriptions"),
    path("card/download_card", views.download_card, name="download_card"),
    path("", views.IndexView.as_view(), name="index"),
]
