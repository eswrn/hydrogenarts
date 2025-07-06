import os
import shutil

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_GEN = os.path.join(BASE_DIR, 'image_generator', 'templates', 'generated_images')
MEDIA_GEN = os.path.join(BASE_DIR, 'media', 'generated_images')

# Create media/generated_images if it doesn't exist
os.makedirs(MEDIA_GEN, exist_ok=True)

# Move all files from templates/generated_images to media/generated_images
if os.path.exists(TEMPLATES_GEN):
    for fname in os.listdir(TEMPLATES_GEN):
        src = os.path.join(TEMPLATES_GEN, fname)
        dst = os.path.join(MEDIA_GEN, fname)
        if os.path.isfile(src):
            print(f"Moving {src} -> {dst}")
            shutil.move(src, dst)
else:
    print(f"Source folder {TEMPLATES_GEN} does not exist.")

print("Done. All images moved to media/generated_images.")
