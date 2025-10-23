from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ImageItem
from .serializers import ImageItemSerializer, ImageItemListSerializer
from .services.cloudinary_service import upload_image_to_cloudinary, delete_image_from_cloudinary

class ImageItemViewSet(viewsets.ModelViewSet):
    """
    API для работы с изображениями:
    - GET /api/images/         -> список всех изображений
    - GET /api/images/<id>/    -> детальная информация
    - POST /api/images/        -> загрузка нового изображения
    - DELETE /api/images/<id>/ -> удаление изображения
    - PATCH /api/images/<id>/  -> изменение данных об изображении
    """
    queryset = ImageItem.objects.all().order_by('-uploaded_at')

    def get_serializer_class(self):
        if self.action == 'list':
            return ImageItemListSerializer  # для списка
        return ImageItemSerializer  # для POST/GET detail и т.д.

    def create(self, request, *args, **kwargs):
        """
        Переопределяем POST для обработки файла и загрузки в Cloudinary
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Получаем файл из запроса
        image_file = request.FILES.get('image_file')
        if not image_file:
            return Response({"error": "image_file is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Загружаем в Cloudinary
        result = upload_image_to_cloudinary(image_file, folder='images')
        serializer.validated_data['image_url'] = result['url']
        serializer.validated_data['cloudinary_public_id'] = result['public_id']

        # Создаём объект модели
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        """
        Удаляем запись из базы и соответствующее изображение из Cloudinary.
        """
        instance = self.get_object()  # получаем объект по pk
        public_id = instance.cloudinary_public_id

        # Удаляем изображение из Cloudinary
        if public_id:
            delete_image_from_cloudinary(public_id)

        # Удаляем объект из базы
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
