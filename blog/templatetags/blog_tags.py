from django import template
from ..models import Post

register = template.Library()


@register.inclusion_tag('_homepage_recent_posts.html')
def home_recent_posts(num):
  """
  Return the specified number of recent blog posts in a partial template
  specifically for inclusion into the Homepage App index.html template
  or a landing page.
  """
  recent_posts = Post.objects.published()[:num]
  return {'recent_posts': recent_posts}