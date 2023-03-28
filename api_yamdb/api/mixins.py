from rest_framework import mixins, viewsets, serializers

from reviews.validators import validate_username


class ListGreateDeleteViewSet(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


class UsernameValidate(serializers.BaseSerializer):

    def validate_username(self, value):
        return validate_username(value)
