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

    # Initial page load
    return render(request, 'image_generator/generate.html')
