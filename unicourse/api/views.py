from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .models import User, Lecture
from .serializers import UserSerializer, LectureSerializer

# Custom permission for admin-only access
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

# Custom permission for teachers or admins
class IsTeacherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['teacher', 'admin']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsTeacherOrAdmin()]
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