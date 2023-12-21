from rest_framework import generics

from product.models import MenuItem, Category, Menu
from .serializer import MenuItemSerializer, CategorySerializer, MenuSerializer, OrderSerializer, OrderItemSerializer,OrderListSerializer
from orders.models import Order, OrderItem, SelectedChoice
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from .authentication import customAuthentication, CustomTokenAuthentication
from .serializer import CustomAuthTokenSerializer, UserSerializerModel, PostOrderSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils import timezone
from rest_framework.views import APIView
from account.models import User
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions
from django.shortcuts import get_object_or_404
import json

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]



class MenuList(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.AllowAny]


class MenuListByCategory(generics.ListAPIView):
    serializer_class = MenuSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        category_id = self.kwargs['id']
        category = get_object_or_404(Category, id=category_id)
        return Menu.objects.filter(categoryId=category.id)


class MenuItemList(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.AllowAny]


    def get_queryset(self):
        menu_id = self.kwargs.get('id')
        if menu_id is not None:
            return MenuItem.objects.filter(menu_id=menu_id)
        return super().get_queryset() 


# class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = NoteModel.objects.all()
#     permission_classes = []
#     serializer_class = NoteSerializer

class PostOrder(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = PostOrderSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Optionally, access and manipulate the validated data
        validated_data = dict(serializer.validated_data)
        order = Order.objects.create(
            Name=validated_data['Name'],
            email=validated_data['email'],
            address=validated_data['address'],
            total=validated_data['total'],
            quantity=validated_data['quantity'],
            user=validated_data['user']
        )

        for item in validated_data['item']:
            order_item = OrderItem.objects.create(
                item=item['item'],
                quantity=item['quantity']
            )
            # print(order_item)
            

            for choice in item['selectedChoices']:
                productid = item['item']
                print(productid)
                SelectedChoice.objects.create(
                    choice=choice['choice'],
                    option=choice['option'],
                    price=choice['price'],
                    order_item=order_item
                )

            order.item.add(order_item)

        # print(order.total)
        # print(order.item)
        # print(f"Order Items: {order.item.all()}")
        order.save()
            


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

# class Orders(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer


class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [permissions.AllowAny]
    

    def get_object(self):
        queryset = self.get_queryset()
        lookup_value = self.kwargs[self.lookup_field]
        obj = generics.get_object_or_404(queryset, id=lookup_value)

        # Perform ownership check
        print(self.request.user.id)
        print(obj.user.id)
        if obj.user.id != self.request.user.id:
            raise PermissionDenied("You do not have permission to access this order.")

        self.check_object_permissions(self.request, obj)
        return obj


class OrderRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    lookup_field = 'id'

    def get_object(self):
        queryset = self.get_queryset()
        lookup_value = self.kwargs[self.lookup_field]
        obj = generics.get_object_or_404(queryset, id=lookup_value)

        # Perform ownership check
        print(self.request.user.id)
        print(obj.user.id)
        if obj.user.id != self.request.user.id:
            raise PermissionDenied("You do not have permission to access this order.")

        self.check_object_permissions(self.request, obj)
        return obj



class OrderItems(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.AllowAny]



class UsersView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializerModel


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializerModel(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])  # Hash the password
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        error_messages = []
        for field, errors in serializer.errors.items():
            for error in errors:
                capitalized_field = field[0].upper() + field[1:]
                error_messages.append(f'{capitalized_field} : {error}')

        error_response = {
            'error': 'Bad Request',
            'details': 'There was an error with your request. Please check the provided data.',
            'errors': error_messages,
        }
        return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)


class ApiLogin(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = (CustomTokenAuthentication, )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = customAuthentication().authenticate(request, username=serializer.validated_data['email'], password=serializer.validated_data['password'])
            if user:
                # Delete any existing tokens for the user
                Token.objects.filter(user=user).delete()

                # Create a new token for the user with an expiry time
                token = Token.objects.create(user=user)
                expiry_time = timezone.now() + timezone.timedelta(minutes=30) # Change this to 2 hours for production
                token.expires = expiry_time
                token.save()


                user_orders = []
                orders = Order.objects.filter(user=user)
                for order in orders:
                    order_data =  OrderSerializer(order).data
                    user_orders.append(json.loads(json.dumps(order_data)))
                
                # print(user_orders)

                user_data = UserSerializerModel(user).data

                return Response({'user': user_data, 'orders' : user_orders, 'token': token.key, 'expires': expiry_time})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Handle validation errors
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    capitalized_field = field[0].upper() + field[1:]
                    error_messages.append(f'{capitalized_field} : {error}')

            error_response = {
                'error': 'Bad Request',
                'details': 'There was an error with your request. Please check the provided data.',
                'errors': error_messages,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)