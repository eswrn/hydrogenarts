from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
import time
from .models import ImageRequest

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.conf import settings
import os

@csrf_exempt
@require_http_methods(["GET", "POST"])
def generate_image(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        user = request.user if request.user.is_authenticated else None
        # Always store image_path relative to MEDIA_ROOT, e.g. generated_images/xxx.jpg
        img_req = ImageRequest.objects.create(prompt=prompt, process=None, user=user)
        return JsonResponse({'request_id': img_req.id, 'status': 'created'})

    # AJAX polling: GET /?request_id=xxx
    request_id = request.GET.get('request_id')
    if request_id:
        img_req = get_object_or_404(ImageRequest, id=request_id)
        if img_req.process == 'done' and img_req.image_path:
            # Always return image_path relative to MEDIA_URL
            image_path = img_req.image_path
            # If image_path is absolute, strip MEDIA_ROOT
            if image_path and os.path.isabs(image_path):
                media_root = os.path.abspath(settings.MEDIA_ROOT)
                if image_path.startswith(media_root):
                    image_path = image_path[len(media_root):].lstrip(os.sep)
            return JsonResponse({'status': 'done', 'image_path': image_path})
        else:
            return JsonResponse({'status': img_req.process or 'pending'})

    # Initial page load or gallery AJAX refresh
    user_generated_images = []
    if request.user.is_authenticated:
        user_images = ImageRequest.objects.filter(user=request.user, process='done').exclude(image_path__isnull=True).exclude(image_path='').order_by('-created_at')
        media_root = os.path.abspath(settings.MEDIA_ROOT)
        for img in user_images:
            image_path = img.image_path
            if image_path and os.path.isabs(image_path):
                idx = image_path.find('media' + os.sep)
                if idx != -1:
                    image_path = image_path[idx:]
            if image_path:
                if not image_path.startswith('/') and not image_path.startswith('media/'):
                    image_path = f'media/{image_path}'
                elif image_path.startswith('generated_images/'):
                    image_path = f'media/{image_path}'
            user_generated_images.append({
                'url': image_path,
                'created_at': img.created_at,
                'prompt': img.prompt,
            })

    # If AJAX gallery refresh, return only the gallery items partial
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.GET.get('gallery') == '1':
        from django.template.loader import render_to_string
        html = render_to_string('image_generator/_gallery_items.html', {'user_generated_images': user_generated_images})
        from django.http import HttpResponse
        return HttpResponse(html)

    return render(request, 'image_generator/generate.html', {
        'user_generated_images': user_generated_images
    })
