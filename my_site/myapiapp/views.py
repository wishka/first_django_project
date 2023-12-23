from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from .serializers import GroupSerializer
from rest_framework.mixins import ListModelMixin


@api_view()
def hello_world_view(request: Request) -> Response:
    return Response({"message": "Hello World"})


class GroupsListView(ListCreateAPIView, GenericAPIView):
    queryset = Group.objects.all() # ListModelMixin позволяет упростить код. Передадим объект, который возвращается
    serializer_class = GroupSerializer # И сериалайзер, который его обрабатывает
# ListCreateAPIView - позволяет еще больше упросить код, так как в состав входит ListModelMixin и ApiView

