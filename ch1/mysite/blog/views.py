from django.shortcuts import render, reverse

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger

from django.views.generic import ListView
from .models import Post
# Create your views here.


class PostView(ListView):
	model = Post
	context_object_name = 'page'
	paginate_by = 3
	template_name = 'blog/post/list.html'


def post_list(request):
	obj_list = Post.published.all()
	pagination_num = 3
	paginator = Paginator(obj_list, pagination_num)
	page_idx = request.GET.get('page_idx')
	
	try:
		page = paginator.page(page_idx)
	
	except EmptyPage:
		page = paginator.page(paginator.num_pages)

	except PageNotAnInteger:
		page = paginator.page(1)

	context = {
		'page': page,
	}

	print('#####:', paginator.count)
	print('#####:', page.has_next())

	return render(request,
					'blog/post/list.html',
					context=context)

def post_detail(request, year, month, day, post):
	post = get_objects_or_404(Post, slug=post,
									status='published',
									publish__year=year,
									published__month=month,
									poublish__day=day)

	#context
	context = {
		'post': post,
	}
	return render(request,
					'blog/post/detail.html',
					context=context)