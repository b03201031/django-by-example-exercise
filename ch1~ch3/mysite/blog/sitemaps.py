from django.contrib.sitemaps import Sitemap

from .models import Post

class PostSiteMap(Sitemap):
	changefreq = 'weekly'
	priority = 0.9

	# call get_absolute_url() to get URL of obj
	def items(self):
		return Post.published.all()

	#  get item obj and return update time
	def lastmod(self, obj):
		return obj.updated