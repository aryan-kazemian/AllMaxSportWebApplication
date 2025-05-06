from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser, MultiPartParser
from .models import Blog, Tag, SEOStatus, Category
from django.db.models import Q
from urllib.parse import urlparse
import os


@csrf_exempt
def blog_api(request):
    if request.method == 'GET':
        if request.GET.get('tags') == 'true':
            tags = Tag.objects.all().values('id', 'name')
            return JsonResponse(list(tags), safe=False)

        filters = {}
        if 'id' in request.GET:
            filters['id'] = request.GET.get('id')
        if 'title' in request.GET:
            filters['title__icontains'] = request.GET.get('title')
        if 'status' in request.GET:
            filters['status'] = request.GET.get('status')
        if 'seo_score' in request.GET:
            filters['seo_score'] = request.GET.get('seo_score')
        if 'seo_score_color' in request.GET:
            filters['seo_score_color'] = request.GET.get('seo_score_color')

        blogs = Blog.objects.filter(**filters).prefetch_related('tags').select_related('seo_status', 'category')
        if 'tags' in request.GET:
            tag_name = request.GET.get('tags')
            blogs = blogs.filter(tags__name__icontains=tag_name)

        result = []
        for blog in blogs:
            seo = getattr(blog, 'seo_status', None)
            cat = blog.category
            result.append({
                'id': blog.id,
                'title': blog.title,
                'author': blog.author,
                'content': blog.content,
                'excerpt': blog.excerpt,
                'meta_description': blog.meta_description,
                'keywords': blog.keywords,
                'status': blog.status,
                'tags': list(blog.tags.values('id', 'name')),
                'featured_image': blog.featured_image,  # <-- now it’s a single string ✅
                'modify_date': blog.modify_date,
                'seo_score': blog.seo_score,
                'seo_score_color': blog.seo_score_color,
                'seo_status': {
                    'title_length_status': seo.title_length_status if seo else None,
                    'title_length_message': seo.title_length_message if seo else None,
                    'content_length_status': seo.content_length_status if seo else None,
                    'content_length_message': seo.content_length_message if seo else None,
                    'keyword_density_status': seo.keyword_density_status if seo else None,
                    'keyword_density_message': seo.keyword_density_message if seo else None,
                    'meta_description_status': seo.meta_description_status if seo else None,
                    'meta_description_message': seo.meta_description_message if seo else None,
                    'headings_status': seo.headings_status if seo else None,
                    'headings_message': seo.headings_message if seo else None,
                    'images_status': seo.images_status if seo else None,
                    'images_message': seo.images_message if seo else None,
                    'internal_links_status': seo.internal_links_status if seo else None,
                    'internal_links_message': seo.internal_links_message if seo else None,
                },
                'category': {
                    'id': cat.id,
                    'category': cat.name
                } if cat else None
            })
        return JsonResponse(result, safe=False)

    elif request.method == 'POST':
        data = request.POST if request.content_type.startswith('multipart') else JSONParser().parse(request)
        files = request.FILES if request.content_type.startswith('multipart') else None

        if request.GET.get('tag') == 'true':
            tag_name = data.get('tag_name')
            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                return JsonResponse({'id': tag.id, 'name': tag.name, 'created': created})
            return JsonResponse({'error': 'tag_name required'}, status=400)

        required_fields = ['title', 'status', 'category']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'error': f'{field} is required'}, status=400)

        category_name = data.get('category')
        category, _ = Category.objects.get_or_create(name=category_name)

        featured_image = data.get('featured_image', '')
        if isinstance(featured_image, list):
            featured_image = featured_image[0] if featured_image else ''

        blog = Blog.objects.create(
            title=data['title'],
            author=data.get('author'),
            content=data.get('content', ''),
            excerpt=data.get('excerpt', ''),
            meta_description=data.get('meta_description', ''),
            keywords=data.get('keywords', ''),
            status=data.get('status', 'draft'),
            seo_score=data.get('seo_score', 0),
            seo_score_color=data.get('seo_score_color', 'text-gray-500'),
            featured_image=featured_image,  # <-- save single URL ✅
            category=category
        )

        tag_names = data.get('tags', [])
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            blog.tags.add(tag)

        seo_data = data.get('seo_status')
        if seo_data:
            SEOStatus.objects.create(
                blog=blog,
                title_length_status=seo_data.get('title_length_status', 'ok'),
                title_length_message=seo_data.get('title_length_message', ''),
                content_length_status=seo_data.get('content_length_status', 'ok'),
                content_length_message=seo_data.get('content_length_message', ''),
                keyword_density_status=seo_data.get('keyword_density_status', 'ok'),
                keyword_density_message=seo_data.get('keyword_density_message', ''),
                meta_description_status=seo_data.get('meta_description_status', 'ok'),
                meta_description_message=seo_data.get('meta_description_message', ''),
                headings_status=seo_data.get('headings_status', 'ok'),
                headings_message=seo_data.get('headings_message', ''),
                images_status=seo_data.get('images_status', 'ok'),
                images_message=seo_data.get('images_message', ''),
                internal_links_status=seo_data.get('internal_links_status', 'ok'),
                internal_links_message=seo_data.get('internal_links_message', ''),
            )
        return JsonResponse({'message': 'Blog created', 'id': blog.id}, status=201)

    elif request.method == 'PATCH':
        data = request.POST if request.content_type.startswith('multipart') else JSONParser().parse(request)
        files = request.FILES if request.content_type.startswith('multipart') else None

        if 'id' in request.GET:
            try:
                blog = Blog.objects.get(id=request.GET.get('id'))

                for field in ['title', 'author', 'content', 'excerpt', 'meta_description', 'keywords', 'status',
                              'seo_score', 'seo_score_color']:
                    if field in data:
                        setattr(blog, field, data[field])

                if 'category_id' in data:
                    try:
                        cat = Category.objects.get(id=data['category_id'])
                        blog.category = cat
                    except Category.DoesNotExist:
                        return JsonResponse({'error': 'Category not found'}, status=404)

                if 'featured_image' in data:
                    featured_image = data.get('featured_image', '')
                    if isinstance(featured_image, list):
                        featured_image = featured_image[0] if featured_image else ''
                    blog.featured_image = featured_image  # <-- save single URL ✅

                blog.save()

                if hasattr(blog, 'seo_status'):
                    seo_data = data.get('seo_status')
                    if seo_data:
                        seo = blog.seo_status
                        for field in [
                            'title_length_status', 'title_length_message',
                            'content_length_status', 'content_length_message',
                            'keyword_density_status', 'keyword_density_message',
                            'meta_description_status', 'meta_description_message',
                            'headings_status', 'headings_message',
                            'images_status', 'images_message',
                            'internal_links_status', 'internal_links_message'
                        ]:
                            if field in seo_data:
                                setattr(seo, field, seo_data[field])
                        seo.save()

                return JsonResponse({'message': 'Blog and SEOStatus updated successfully'})
            except Blog.DoesNotExist:
                return JsonResponse({'error': 'Blog not found'}, status=404)

    elif request.method == 'DELETE':
        if 'id' in request.GET:
            try:
                blog = Blog.objects.get(id=request.GET.get('id'))
                blog.delete()
                return JsonResponse({'message': 'Blog deleted successfully'})
            except Blog.DoesNotExist:
                return JsonResponse({'error': 'Blog not found'}, status=404)

        elif 'category_id' in request.GET:
            try:
                category = Category.objects.get(id=request.GET.get('category_id'))
                category.delete()
                return JsonResponse({'message': 'Category deleted successfully'})
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Category not found'}, status=404)

        else:
            return JsonResponse({'error': 'No id or category_id provided'}, status=400)

    return JsonResponse({'message': 'Method not allowed'}, status=405)
