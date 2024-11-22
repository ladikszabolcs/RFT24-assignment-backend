from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Lecture
from .serializers import UserSerializer, LectureSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAdminUser() | permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        lecture = self.get_object()
        if request.user.role == 'student' and lecture.students.count() < lecture.max_students:
            lecture.students.add(request.user)
            return Response({'status': 'applied'})
        return Response({'status': 'failed'}, status=400)

    @action(detail=True, methods=['post'])
    def unapply(self, request, pk=None):
        lecture = self.get_object()
        if request.user.role == 'student':
            lecture.students.remove(request.user)
            return Response({'status': 'unapplied'})
        return Response({'status': 'failed'}, status=400)