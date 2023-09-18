from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.decorators import action


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from common.permissions import IsAdminOrReadOnly
from posts.filters import PostFilter

from posts.models import Post
from posts.serializers import CommentSerializer, PostSerializer

from users.models import Follow, Profile, User
from users.serializers import (
    UserProfileSerializer,
    ProfileSerializer,
    SignUpSeiralizer,
    LoginSeiralizer,
    UserInfoSerializer,
    UserSerializer,
    FollowSerializer,
)
from users.filters import UserFilter, ProfileFilter, FollowFilter
from users import openapi


@extend_schema(tags=["00. Auth"], **openapi.sign_up)
class SignUpView(APIView):
    serializer_class = SignUpSeiralizer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            return Response(
                {
                    "user": serializer.data,
                    "detail": "register successs",
                    "token": {"access": access_token, "refresh": refresh_token},
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["00. Auth"], **openapi.login)
class LoginView(APIView):
    serializer_class = LoginSeiralizer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            serializer = self.serializer_class(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            return Response(
                {
                    "user": serializer.data,
                    "detail": "login successs",
                    "token": {"access": access_token, "refresh": refresh_token},
                },
                status=status.HTTP_200_OK,
            )
        return Response({"detail": "login failed"}, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(tags=["00. Auth"], **openapi.create_token)
class TokenObtainPairView_(TokenObtainPairView):
    pass


@extend_schema(tags=["00. Auth"], **openapi.refresh_token)
class TokenRefreshView_(TokenRefreshView):
    pass


@extend_schema(tags=["03. User"])
@extend_schema_view(
    list=extend_schema(**openapi.user_list),
    create=extend_schema(**openapi.user_create),
    retrieve=extend_schema(**openapi.user_retrieve),
    update=extend_schema(**openapi.user_update),
    partial_update=extend_schema(**openapi.user_partial_update),
    destroy=extend_schema(**openapi.user_destroy),
)
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter

    def get_queryset(self):
        user: User = self.request.user
        queryset = (
            self.queryset if user.is_admin else self.queryset.filter(is_active=True)
        )

        return queryset

    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(deprecated=True)
    def create(self, request: Request, *args, **kwargs):
        return Response(
            data={"detail": "Create operation is not supported"},
            status=status.HTTP_404_NOT_FOUND,
        )

    @extend_schema(tags=["05. Follow"], **openapi.user_follow)
    @action(
        detail=True,
        methods=["post"],
        url_path=r"follow/(?P<id>[0-9]+)",
    )
    def follow(self, request: Request, pk, id):
        follower: User = get_object_or_404(User, id=pk, is_active=True)
        followee: User = get_object_or_404(User, id=id, is_active=True)

        follow, created = Follow.objects.get_or_create(
            user_from=follower, user_to=followee
        )

        if created:
            return Response(
                data={"detail": "Follow successfully"}, status=status.HTTP_201_CREATED
            )

        follow.delete()

        return Response(
            data={"detail": "Unfollowed successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @extend_schema(tags=["05. Follow"], **openapi.user_following)
    @action(detail=True, methods=["get"], url_name="following")
    def following(self, request: Request, *args, **kwargs):
        user: User = self.get_object()

        following = (
            user.following.all()
            if request.user.is_admin
            else user.following.filter(is_active=True)
        )
        serializer = self.get_serializer(following, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=["05. Follow"], **openapi.user_follower)
    @action(detail=True, methods=["get"], url_name="follower")
    def follower(self, request: Request, *args, **kwargs):
        user: User = self.get_object()

        following = (
            user.follower.all()
            if request.user.is_admin
            else user.follower.filter(is_active=True)
        )
        serializer = self.get_serializer(following, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=["06. Post"], **openapi.user_posts)
    @action(detail=True, methods=["get"], url_name="posts")
    def posts(self, request: Request, *args, **kwargs):
        user: User = self.get_object()
        posts = (
            user.posts.all()
            if request.user.is_admin
            else user.posts.filter(status=Post.StatusChoices.PUBLISHED, is_active=True)
        )

        serializer = PostSerializer(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=["06. Post"], **openapi.user_feed)
    @action(detail=True, methods=["get"], url_path="feed")
    def feed(self, request: Request, *args, **kwargs):
        user: User = self.get_object()
        following = user.following.all()
        posts = (
            Post.objects.filter(author__in=following)
            if request.user.is_admin
            else Post.objects.filter(
                author__in=following,
                status=Post.StatusChoices.PUBLISHED,
                is_active=True,
            )
        )

        serializer = PostSerializer(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=["07. Comment"], **openapi.user_comments)
    @action(detail=True, methods=["get"], url_name="comments")
    def comments(self, request: Request, *args, **kwargs):
        user: User = self.get_object()
        comments = (
            user.comments.all()
            if request.user.is_admin
            else user.comments.filter(is_active=True)
        )

        serializer = CommentSerializer(comments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["04. Profile"])
class ProfileView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = UserProfileSerializer

    def get(self, request, user_pk):
        user: User = get_object_or_404(User, id=user_pk, is_active=True)
        profile: Profile = (
            get_object_or_404(Profile, user=user)
            if user.is_admin
            else get_object_or_404(Profile, user=user, is_active=True)
        )

        serializer = self.serializer_class(profile)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_pk):
        user: User = get_object_or_404(User, id=user_pk, is_active=True)
        serializer = self.serializer_class(data=request.data, context={"user": user})

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, user_pk):
        user: User = get_object_or_404(User, id=user_pk, is_active=True)
        instance: Profile = get_object_or_404(Profile, user=user, is_active=True)
        serializer = self.serializer_class(instance, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_pk):
        user: User = get_object_or_404(User, id=user_pk, is_active=True)
        profile: Profile = get_object_or_404(Profile, user=user, is_active=True)

        profile.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["05. Follow"])
class FollowListView(APIView):
    serializer_class = FollowSerializer
    filter_backends = DjangoFilterBackend
    filterset_class = FollowFilter

    def get(self, request):
        follow: Follow = Follow.objects.all()
        queryset = self.filter_backends().filter_queryset(request, follow, self)

        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["01. My"])
class MyInfoView(APIView):
    serializer_class = UserInfoSerializer

    def get(self, request):
        user: User = request.user

        serializer = self.serializer_class(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = self.serializer_class(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["01. Others"])
class OtherUserInfoView(APIView):
    serializer_class = UserInfoSerializer

    def get(self, request):
        users: User = (
            User.objects.select_related("profile")
            .filter(is_active=True)
            .exclude(id=request.user.id)
        )

        serializer = self.serializer_class(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["01. My"])
class MyProfileView(APIView):
    serializer_class = ProfileSerializer

    def get(self, request):
        user: User = request.user
        profile = user.profile

        serializer = self.serializer_class(profile)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        serializer = self.serializer_class(request.user.profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["01. Others"])
class OtherProfileView(APIView):
    serializer_class = ProfileSerializer
    filter_backends = DjangoFilterBackend
    filterset_class = ProfileFilter

    def get(self, request):
        profile: Profile = Profile.objects.filter(is_active=True).exclude(
            user=request.user
        )
        queryset = self.filter_backends().filter_queryset(request, profile, self)

        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["01. My"])
class MyFollowView(APIView):
    def post(self, request, user_id):
        user: User = request.user

        followee = get_object_or_404(User, id=user_id, is_active=True)
        follow, created = Follow.objects.get_or_create(user_from=user, user_to=followee)

        if created:
            return Response(
                data={"detail": "Followed successfully"},
                status=status.HTTP_201_CREATED,
            )

        follow.delete()

        return Response(
            data={"detail": "Unfollowed successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


@extend_schema(tags=["01. My"])
class MyFollowingView(APIView):
    serializer_class = UserSerializer
    filter_backends = DjangoFilterBackend
    filterset_class = UserFilter

    def get(self, request):
        user: User = request.user
        following = user.following.filter(is_active=True)
        queryset = self.filter_backends().filter_queryset(request, following, self)

        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["01. My"])
class MyFollowerView(APIView):
    serializer_class = UserSerializer
    filter_backends = DjangoFilterBackend
    filterset_class = UserFilter

    def get(self, request):
        user: User = request.user
        follower = user.follower.filter(is_active=True)
        queryset = self.filter_backends().filter_queryset(request, follower, self)

        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
