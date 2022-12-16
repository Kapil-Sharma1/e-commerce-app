from django.urls import path
from users.views import RegisterApi, UserRetrieveAPIView, LogOutApiView

urlpatterns = [
      path('api/register', RegisterApi.as_view()),
      path('<int:User_id>',UserRetrieveAPIView.as_view() ),
      path('api/logout', LogOutApiView.as_view() )
]