from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .models import User, Lecture
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, LectureSerializer

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Delete any existing tokens for the user
        Token.objects.filter(user=user).delete()

        # Create a new token
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email
        })
# Custom permission for admin-only access
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

# Custom permission for teachers or admins
class IsTeacherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['teacher', 'admin']


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Use the authenticated user
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # All users must be authenticated

    def get_permissions(self):
        if self.action == 'list':  # Restrict list action
            return [IsAdmin()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response(
                {'error': 'You do not have permission to view the user list.'},
                status=403
            )
        return super().list(request, *args, **kwargs)

class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsTeacherOrAdmin()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'], url_path='enroll')
    def enroll(self, request, pk=None):
        """Enroll the authenticated student in a lecture."""
        lecture = self.get_object()
        user = request.user

        # Ensure the user is a student
        if user.role != 'student':
            return Response({'error': 'Only students can enroll in lectures.'}, status=403)

        # Check if the lecture has available slots
        if lecture.students.count() >= lecture.max_students:
            return Response({'error': 'This lecture is already full.'}, status=400)

        # Check if the student is already enrolled
        if lecture.students.filter(id=user.id).exists():
            return Response({'error': 'You are already enrolled in this lecture.'}, status=400)

        # Enroll the student
        lecture.students.add(user)
        return Response({'message': 'You have been successfully enrolled.'}, status=200)

    @action(detail=True, methods=['post'], url_path='unenroll')
    def unenroll(self, request, pk=None):
        """Unenroll the authenticated student from a lecture."""
        lecture = self.get_object()
        user = request.user

        # Ensure the user is a student
        if user.role != 'student':
            return Response({'error': 'Only students can unenroll from lectures.'}, status=403)

        # Check if the student is enrolled in the lecture
        if not lecture.students.filter(id=user.id).exists():
            return Response({'error': 'You are not enrolled in this lecture.'}, status=400)

        # Unenroll the student
        lecture.students.remove(user)
        return Response({'message': 'You have been successfully unenrolled.'}, status=200)