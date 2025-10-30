import logging
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser

from rest_framework.viewsets import ModelViewSet
from . import serializers
from ..db import models

logger = logging.getLogger(f"ccp4x:{__name__}")


class FileUseViewSet(ModelViewSet):
    queryset = models.FileUse.objects.all()
    serializer_class = serializers.FileUseSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]
