from django.urls import path

from . import views


url_patterns = [
    # admin views
    # APIs
    path('', views.ListObjects.as_view()),
    path('<int:pk>', views.RetrieveObject.as_view()),
    path('type/', views.TypeObjectListAPIView.as_view()),
    path('type/<int:pk>', views.TypeObjectListAPIView.as_view()),

    path('category/', views.CategoryListAPIView.as_view()),
    path('category/<int:pk>', views.CategoryRetrieveAPIView.as_view()),

    path('region/', views.RegionListAPIView.as_view()),
    path('region/<int:pk>', views.RegionRetrieveAPIView.as_view()),

    path('banner/', views.BannerListAPIView.as_view()),
    path('banner/<int:pk>', views.BannerRetrieveAPIView.as_view()),

    path('service/', views.ServiceListAPIView.as_view()),
    path('service/<int:pk>', views.ServiceRetrieveAPIView.as_view()),

    path('inventory/', views.InventoryListAPIView.as_view()),
    path('inventory/<int:pk>', views.InventoryRetrieveAPIView.as_view()),

    path('metro/', views.MetroListAPIView.as_view()),
    path('metro/<int:pk>', views.MetroRetrieveAPIView.as_view()),

    path('object-service/', views.ObjectServicesListAPIView.as_view()),
    path('object-service/<int:pk>', views.ObjectServiceRetrieveAPIView.as_view()),

    path('object-inventory/', views.ObjectInventoryListAPIView.as_view()),
    path('object-inventory/<int:pk>', views.ObjectInventoryListAPIView.as_view()),

    path('bathroom-types/', views.BathroomTypesList.as_view()),

    path('views-from-window-types/', views.ViewFromWindowList.as_view()),
]