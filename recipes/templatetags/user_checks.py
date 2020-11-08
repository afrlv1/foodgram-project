from django import template

register = template.Library()


@register.filter
def check_subscription(user_obj, author):
    return user_obj.is_following(author)
