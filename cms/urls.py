from django.urls import path,include

urlpatterns = [
    path('', include("houtai.urls")),
    path('', include("pc.urls")),

]
