from rest_framework.generics import CreateAPIView

from .serializers import VacancyApplicationPostSerializer

class VacancyPostAPIView(CreateAPIView):
    serializer_class = VacancyApplicationPostSerializer