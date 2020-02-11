from rest_framework.mixins import ListModelMixin, DestroyModelMixin
from rest_framework import viewsets, mixins


from core.models import Ingredient, Recipe

from recipe import serializers


class RecipeViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        name_param = self.request.query_params.get('name')
        queryset = self.queryset
        if name_param:
            queryset = queryset.filter(name__contains=name_param)

        return queryset
