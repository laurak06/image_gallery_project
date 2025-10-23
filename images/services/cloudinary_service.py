from decouple import config
import cloudinary
import cloudinary.uploader

# Настройка Cloudinary через переменные окружения (.env)
cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET'),
    secure=True
)

def upload_image_to_cloudinary(file_obj, folder=None, public_id=None):
    """
    Загружает файл в Cloudinary.
    Возвращает словарь с URL, public_id и всей "сырой" информацией от Cloudinary.
    """
    options = {}
    if folder:
        options['folder'] = folder
    if public_id:
        options['public_id'] = public_id

    result = cloudinary.uploader.upload(file_obj, **options)

    return {
        'url': result.get('secure_url') or result.get('url'),
        'public_id': result.get('public_id'),
        'raw': result
    }

def delete_image_from_cloudinary(public_id):
    """
    Удаляет изображение из Cloudinary по его public_id.
    """
    return cloudinary.uploader.destroy(public_id)
