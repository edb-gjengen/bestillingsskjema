from rest_framework.serializers import ModelSerializer
from bestilling.models import Attachment


class AttachmentSerializer(ModelSerializer):

    class Meta:
        model = Attachment
        fields = ('id', 'uploaded_file', 'trello_id', 'object_id', 'content_type')
        read_only_fields = ('id',)
