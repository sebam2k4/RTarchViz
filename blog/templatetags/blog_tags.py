from django import template
from ..models import Post

register = template.Library()


@register.inclusion_tag('_homepage_recent_posts.html')
def home_recent_posts():
  """
  Return the last 5 blog posts in a partial template specifically for
  inclusion into the Homepage App index.html template or a landing page.
  """
  recent_posts = Post.objects.published()[:5]
  return {'recent_posts': recent_posts}