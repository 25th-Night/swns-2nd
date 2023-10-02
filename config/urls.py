"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from users.views import (
    MyInfoView,
    OtherUserInfoView,
    MyProfileView,
    OtherProfileView,
    MyFollowView,
    MyFollowingView,
    MyFollowerView,
)

from posts.views import (
    OtherPostListView,
    MyPostListView,
    MyFeedView,
    MyCommentListView,
    OtherImageListView,
    MyImageListView,
    LikePostView,
    LikeCommentView,
    MyLikePostListView,
    MyLikeCommentListView,
)


urlpatterns = [
    path("users/", include("users.urls")),
    path("my/info/", MyInfoView.as_view(), name="my_info"),
    path("my/profile/", MyProfileView.as_view(), name="my_profile"),
    path("my/follow/<int:user_id>/", MyFollowView.as_view(), name="my_follow"),
    path("my/following/", MyFollowingView.as_view(), name="my_following"),
    path("my/follower/", MyFollowerView.as_view(), name="my_follower"),
    path("my/feed/", MyFeedView.as_view(), name="my_feed"),
    path("my/posts/", MyPostListView.as_view(), name="my_posts_list"),
    path("my/comments/", MyCommentListView.as_view(), name="my_comments_list"),
    path("my/images/", MyImageListView.as_view(), name="my_images_list"),
    path("my/like/post/<int:post_id>/", LikePostView.as_view(), name="my_like_post"),
    path(
        "my/like/comment/<int:comment_id>/",
        LikeCommentView.as_view(),
        name="my_like_comment",
    ),
    path("my/like/posts/", MyLikePostListView.as_view(), name="my_liked_posts"),
    path(
        "my/like/comments/", MyLikeCommentListView.as_view(), name="my_liked_comments"
    ),
    path("others/info/", OtherUserInfoView.as_view(), name="other_users"),
    path("others/profile/", OtherProfileView.as_view(), name="other_profile"),
    path("others/posts/", OtherPostListView.as_view(), name="other_posts_list"),
    path("others/images/", OtherImageListView.as_view(), name="other_images_list"),
    path("admin/", admin.site.urls),
    path("posts/", include("posts.urls")),
    path("api-auth/", include("rest_framework.urls")),
]

drf_spectacular_urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="api-schema"),
        name="api-redoc",
    ),
]

prometheus_urlpatterns = [
    path("", include("django_prometheus.urls")),
]

urlpatterns += drf_spectacular_urlpatterns + prometheus_urlpatterns
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
