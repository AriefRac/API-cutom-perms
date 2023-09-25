from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, BasePermission, SAFE_METHODS

from main.models import Modul, Post
from .serializers import ModulSerializer, PostSerializer

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
# Create your views here.

class IsOwnerOrAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners or admin to edit and delete posts.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone, so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the post or admin users.
        return obj.author == request.user or request.user.is_staff

class ModulViewSet(viewsets.ModelViewSet):
    queryset = Modul.objects.all()
    serializer_class = ModulSerializer
    permission_classes = [IsAdminUser | IsAuthenticated]  # Admin atau pengguna yang sudah autentikasi

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'success', 'message': 'Success Create data'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'success', 'message': 'Data updated success', 'data': serializer.data}, status=status.HTTP_202_ACCEPTED)

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = Modul.objects.all()

        if user.is_staff:  # Jika pengguna adalah admin, tampilkan semua modul
            pass
        else:
            # Ambil izin-izin yang sesuai dengan kategori modul dan buat daftar izin
            category_permissions = {
                'main.can_view_frontend_modul': 'FrontEnd',
                'main.can_view_backend_modul': 'BackEnd',
                'main.can_view_qa_modul': 'QA',
                'main.can_view_ui/ux_modul': 'UI/UX',
            }
            
            allowed_categories = [category for permission, category in category_permissions.items() if user.has_perm(permission)]
            status = ['published']
            # Filter queryset berdasarkan kategori yang diizinkan
            queryset = queryset.filter(category__name__in=allowed_categories, status__in=status)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'status': 'success', 'message': 'Success listing data', 'data': serializer.data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'status': 'success', 'message': 'Success get detail data', 'data': serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    

class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing Post objects.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'status': 'success', 'message':'Success Create data'}, 
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'status':'success', 'message': 'Data updated success', 'data': serializer.data})

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'status':'success', 'message':'Success listing data', 'data': serializer.data})
     
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'status': 'success', 'message': 'Success get detail data', 'data': serializer.data})
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 

class AddPermissionForUser(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        # Tambahkan kode untuk memberikan izin kepada pengguna berdasarkan post
        post = serializer.instance
        author = post.author

        # Mengecek apakah post memiliki kategori yang valid
        allowed_categories = ['FrontEnd', 'BackEnd', 'QA', 'UI/UX']  # Sesuaikan dengan izin yang Anda definisikan dalam Meta
        if post.category.name in allowed_categories:
            # Mendapatkan nama izin yang sesuai dengan kategori post
            permission_name = f"can_view_{post.category.name.lower()}_modul"

            # Mengecek apakah izin sudah ada, jika belum, maka membuatnya
            content_type = ContentType.objects.get_for_model(Modul)
            permission, created = Permission.objects.get_or_create(
                codename=permission_name,
                name=f"Can view {post.category.name} modules",
                content_type=content_type,
            )

            # Memberikan izin kepada pengguna
            author.user_permissions.add(permission)

        serializer.save()

        return Response({'status': 'success', 'message': 'Permission added successfully'}, status=status.HTTP_200_OK)
    
