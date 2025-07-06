from .models import ImageRequest

def generate_image_from_prompt(prompt):
    """
    Generates an image based on a prompt.
    For now, simulates the generation and returns a path.
    """
    if not prompt:
        return {'error': 'Prompt is required'}, 400

    # Create a new image request object
    image_request = ImageRequest.objects.create(prompt=prompt)

    # TODO: Call the image generation API with the prompt
    # For now, we'll just simulate a successful response
    image_path = f'generated_images/{image_request.id}.jpg'
    image_request.image_path = image_path
    image_request.save()

    return {'image_path': image_path}, 200