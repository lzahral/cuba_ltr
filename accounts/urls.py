from django.urls import include, path
from .views import  *

urlpatterns = [
    # path("api/", include("accounts.api.urls")),


    path('register', Register.as_view(), name='register'),
    # path('profile', EditProfile.as_view(), name='edit-profile'),
    path('list/', UsersListView.as_view(), name='users'),
    path('login/', Login.as_view(), name='login'),
    path('logout', logout_page, name='logout'),
    path('create/', UserCreateView.as_view(), name='new_user'),
    path("edit/<int:pk>/", UserUpdateView.as_view(), name="edit_user"),
    path("delete/<int:pk>/", UserDelete.as_view(), name="delete_user")

    # path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
#     path('change-password/', ChangePassword.as_view(),
#          name='change-password'),

#     path('delete-notification', delete_notification,
#       name='delete-notification'),
#     path('read-all-notification',read_all_notification,
#          name='read-all-notification'),
#     path('delete-all-notification',delete_all_notifications,
#          name='delete-all-notification'),
]
