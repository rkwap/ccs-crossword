from django import template
register = template.Library()

@register.filter(name='formclass')
def formclass(field, css):
   return field.as_widget(attrs={"class":css})

@register.filter(name='split')
def split(value, key):
  """
    Returns the value turned into a list.
  """
  return value.split(key)