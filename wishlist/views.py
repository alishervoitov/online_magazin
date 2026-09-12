from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Wishlist
from .serializers import WishlistSerializer


class WishlistView(generics.ListCreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data.get('product')

        if Wishlist.objects.filter(user=user, product=product).exists():
            return Response({"message": "Bu mahsulot allaqachon sevimlilarga qo'shilgan."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=user)


class WishlistDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)