
from django.shortcuts import render, reverse, get_object_or_404

#models
from django.db.models import Count

#pagination
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger

#email
from django.core.mail import send_mail

#local
from django.views.generic import ListView

from .models import Post
from .forms import EmailPostForm,  CommentForm

from taggit.models import Tag

# Create your views here.

def post_detail(request, year, month, day, post):

	post = get_object_or_404(Post, slug=post,
								   status = 'published',
								   publish__year=year,
								   publish__month=month,
								   publish__day=day)

	# List of comments from related_name
	comments = post.comments.filter(active=True)
	new_comment = None

	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)

		if comment_form.is_valid():
			
			# to get the object instance and save later
			new_comment = comment_form.save(commit=False)
			# add FK
			new_comment.post = post
			new_comment.save()

	else:
		comment_form = CommentForm()



	post_tags_ids = post.tags.values_list('id', flat=True)

	# __in use AND
	# filter no DISTINCT
	similar_posts = Post.published.filter(tags__in=post_tags_ids).distinct()\
									.exclude(id=post.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
									.order_by('-same_tags', '-publish')

	print(similar_posts)

	context = {
		'post': post,
		'comments': comments,
		'new_comment': new_comment,
		'comment_form': comment_form,
		'similar_posts': similar_posts,
	}

	TEMPLATE_PATH = 'blog/post/detail.html'

	return  render(request, TEMPLATE_PATH, context=context)


def post_share(request, post_id):
	post = get_object_or_404(Post, id=post_id,
								   status='published')

	context = dict()

	if request.method == 'POST':

		form = EmailPostForm(request.POST)
		
		if form.is_valid():
			#get form data
			cd = form.cleaned_data

			#send eamil
			print(post.get_absolute_url)
			post_uri = request.build_absolute_uri(location=post.get_absolute_url())
			
			subject = "{}( {} ) recommand you reading '{}'"
			subject = subject.format(cd['name'], cd['email'], post.title)

			message = "Read '{}' at {}\n\n{}\'s commet: {}"
			message = message.format(post.title, post_uri,
										cd['name'], cd['comments'])

			from mysite import local_settings
			host_mail = local_settings.EMAIL_HOST_USER
		
			send_mail(subject, message, host_mail, [cd['to']])
			sent = True
			context['cd'] = cd


	else:
		sent = False
		form = EmailPostForm()

	context['post'] = post
	context['form'] = form
	context['sent'] = sent


	return render(request, 'blog/post/share.html', context=context)



class PostView(ListView):
	model = Post
	context_object_name = 'page'
	paginate_by = 3
	template_name = 'blog/post/list.html'


def post_list(request, page_idx=1, tag_slug=None):

	print(page_idx)
	object_list = Post.published.all()
	tag = None

	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])


	pagination_num = 1
	paginator = Paginator(object_list, pagination_num)
	
	try:
		page_obj = paginator.page(page_idx)
	
	except EmptyPage:
		page_obj = paginator.page(paginator.num_pages)

	except PageNotAnInteger:
		page_obj = paginator.page(1)




	#params setup
	context = {
		'page_obj': page_obj,
		'page_idx': page_idx,
		'tag': tag,
	}

	TEMPLATE_PATH = 'blog/post/list.html'
	
	return render(request,
				  TEMPLATE_PATH,
				  context=context)


