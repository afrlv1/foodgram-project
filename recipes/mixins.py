from django.core.exceptions import PermissionDenied

from recipes.models import Tag, FollowRecipe, ShoppingList


class RecipeObjectMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'all_tags': Tag.objects.all()})

        if self.request.user.is_authenticated:
            context['following_list'] = FollowRecipe.objects.select_related(
                'user', 'recipe'
            ).filter(
                user=self.request.user
            ).values_list(
                'recipe__id', flat=True
            ).distinct()

            context['card_list'] = ShoppingList.objects.select_related(
                'user', 'recipe'
            ).filter(
                user=self.request.user
            ).values_list(
                'recipe__id', flat=True
            ).distinct()

            context['followers'] = self.request.user.follower.all().values_list(
                'author__id', flat=True
            ).distinct()

        return context


class AuthorRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied()
        return super(AuthorRequiredMixin, self).dispatch(request, *args, **kwargs)
