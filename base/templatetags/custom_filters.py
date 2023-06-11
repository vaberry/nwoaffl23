from django import template

register = template.Library()

@register.filter
def create_range(value):
    return range(1, int(value) + 1)

@register.filter
def get_dict_value(dictionary, key):
    # print(dictionary)
    # print(key)
    # show = dictionary.get(str(key), None)
    # print(show)
    return dictionary.get(str(key), None)