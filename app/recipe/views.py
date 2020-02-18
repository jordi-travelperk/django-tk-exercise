from rest_framework import viewsets, mixins
from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    """
    API endpoint that allows recipes to be created, viewed, edited or deleted.
    """

    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Query recipes based on name query param"""
        name_param = self.request.query_params.get('name')
        queryset = self.queryset
        if name_param:
            queryset = queryset.filter(name__contains=name_param)

        return queryset.order_by('-id').distinct()
