from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='get_item')
def get_item(dictionary, key):
    """Récupère un élément d'un dictionnaire par sa clé."""
    return dictionary.get(key)
