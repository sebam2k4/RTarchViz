from django import template
from ..models import Post

register = template.Library()


@register.inclusion_tag('_recent_posts_list_partial.html')
def home_recent_posts(num):
  """
  Return the specified number of recent blog posts in a partial template
  specifically for inclusion into other Apps's template.
  """
  recent_posts = Post.objects.published()[:num]
  return {'recent_posts': recent_posts}