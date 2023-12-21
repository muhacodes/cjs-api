from django.urls import path, include
from .views import MenuList, MenuListByCategory, CategoryList, MenuItemList, OrderViewSet,PostOrder, OrderCreateView, OrderItems, ApiLogin, RegisterView, UsersView, OrderRetrieveAPIView, OrderList
from rest_framework import routers
from rest_framework.routers import DefaultRouter

router = routers.DefaultRouter()
router.register(r'', OrderViewSet)

# router.register(r'users', UsersView)



urlpatterns = [
    path('category', CategoryList.as_view()),
    path('menu', MenuList.as_view()),

    path('category/menu/<int:id>/', MenuListByCategory.as_view()),  # New URL pattern

    path('menu-item', MenuItemList.as_view()),
    path('menu-item/<int:id>', MenuItemList.as_view()),

   


#   

    path('order-post', PostOrder.as_view(), name='post-order'),

   
    path('order-items', OrderItems.as_view(),),
    
    path('orders-create',OrderCreateView.as_view(), name='orders-create' ),
    # path('orders/<int:pk>', OrderCreateView.as_view(), name='order-detail'),

    path('order-list', OrderList.as_view(),),

    path('orders/<int:id>/', OrderRetrieveAPIView.as_view(), name='order-retrieve'),


    path('users/register', RegisterView.as_view()),
    path('users/login', ApiLogin.as_view(),)

]