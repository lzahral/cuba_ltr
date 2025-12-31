from django.urls import path
from .views import *


urlpatterns = [
    path("new/", LetterCreateView.as_view(), name="new_letter"),
    path("list/", Letters.as_view(), name="letters"),
    path("list/<int:pk>/", LetterDetailView.as_view(), name="letter_detail"),
    path("reply/<int:pk>/", ReplyLetterView.as_view(), name="reply"),    
    path("delete/<int:pk>/", DeleteLetterView.as_view(), name="letter_delete"), 
]
