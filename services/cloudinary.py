import cloudinary
import cloudinary.uploader
from config.config import settings

class CloudinaryService:
    def __init__(self):
        cloudinary.config(
            cloud_name=settings.cloudinary_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True
        )

    def upload_image(self, file, public_id: str):
        # Завантажуємо та обрізаємо до квадрата (avatar style)
        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
        src_url = cloudinary.CloudinaryImage(public_id).build_url(
            width=250, height=250, crop='fill', version=r.get('version')
        )
        return src_url

cloudinary_service = CloudinaryService()