from rest_framework import permissions

from shopapp.models import Product


class IsProductAuthor(permissions.BasePermission):
    """
    Custom permission to only allow the author of a product to edit it.
    """
    def has_permission(self, request, view):

        product_id = Product.objects.get('product.pk')  # Замените на то, что соответствует вашей модели продукта
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return False  # В случае отсутствия продукта, разрешение отклоняется

        # Проверяем, является ли текущий пользователь автором продукта
        return product.author == request.user