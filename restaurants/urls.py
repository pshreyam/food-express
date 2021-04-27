from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    # urls for customers to view resturants
    path('', views.restaurant_list, name='restaurant_list'),
    path('category/<slug:category_slug>/', views.restaurant_list, name='restaurant_list_by_category'),
    path('<int:id>/<slug:slug>/', views.restaurant_detail, name='restaurant_detail'),
    # urls for restaurant user to view his/her restaurant
    path('dashboard/<str:username>/', views.restaurant_dashboard, name='restaurant_dashboard'),
    path('profile/<str:username>/', views.update_restaurant_profile, name='update_restaurant_profile' ),
    path('food/create/', views.FoodCreateView.as_view(), name='create_food'),
    path('food/update/<int:pk>/', views.FoodUpdateView.as_view(), name='update_food'),
    path('foods/', views.RestaurantFoodListView.as_view(), name='food_list'),
    path('foods/category/<slug:category_slug>/', views.RestaurantFoodListView.as_view(), name='foods_list_by_category'),
    path('food/<int:pk>/', views.RestaurantFoodDetailView.as_view(), name='food_detail')
]
