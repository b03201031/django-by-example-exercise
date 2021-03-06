from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from taggit.managers import TaggableManager

# Create your models here.

class PublishedManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(status='published')

class Post(models.Model):
	#choices
	STATUS_CHOICE = {
		('draft', 'Draft'),
		('published', 'Published'),
	}


	#field
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250,
							unique_for_date='publish')

	author = models.ForeignKey(User,
								related_name='blog_posts',
								on_delete='CASCADE')

	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,
							  choices=STATUS_CHOICE,
							  default='draft')


	#manager
	objects = models.Manager()
	published = PublishedManager()
	tags = TaggableManager()



	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title


	def get_absolute_url(self):
		args =	[
			self.publish.year,
			self.publish.strftime('%m'),
			self.publish.strftime('%d'),
			self.slug,
		]
		return reverse('blog:post_detail', args=args)




class Comment(models.Model):

	post = models.ForeignKey(Post, related_name='comments',
	 							   on_delete='CASCADE') #related_name use for reverse queryset
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering =('created', )

	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.post)



