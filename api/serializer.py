from rest_framework import serializers

from product.models import MenuItem, Category, Menu, Options, Choices, AddOn
from orders.models import Order, OrderItem, SelectedOption, SelectedChoice

from account.models import User
from django.contrib.auth.password_validation import validate_password

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"




class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = ['id', 'option', 'amount']


class AddOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOn
        fields = ['add_on', 'price']


class ChoicesSerializer(serializers.ModelSerializer):
    options = OptionsSerializer(many=True)
    
    class Meta:
        model = Choices
        fields = ['id', 'name', 'options', 'price']



class MenuItemSerializer(serializers.ModelSerializer):
    choices = ChoicesSerializer(many=True)
    add_ons = AddOnSerializer(many=True)
    
    class Meta:
        model = MenuItem
        fields = ['id', 'menu_id', 'featured', 'title', 'description', 'image_url', 'price', 'choices', 'add_ons']


class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = ["option", "amount"]


# class ItemSerializer(serializers.ModelSerializer):
#     option = OptionsSerializer(many=True)
#     class Meta:
#         model = OrderItem
#         fields = ['item', "quantity" 'options']

#     def create(self, validated_data):
#         pass
    

class UserSerializerModel(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    favorite = MenuItemSerializer(many=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'favorite', 'name', 'address', 'telephone', 'username', 'password']




class OrderItemSerializer(serializers.ModelSerializer):
    # item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    item = MenuItemSerializer()

    class Meta:
        model = OrderItem
        fields = ['quantity', 'item']

    

class SelectedOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedOption
        fields = ['id', 'choice', 'option', 'order_item']


class OrderItemSerializerRaw(serializers.ModelSerializer):
    # item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())

    item = MenuItemSerializer()
    selected_options  = SelectedOptionSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = ['quantity', 'selected_options', 'item']

    def to_representation(self, instance):
        # Custom representation to handle nested serialization of selected options
        representation = super(OrderItemSerializerRaw, self).to_representation(instance)
        representation['selected_options'] = SelectedOptionSerializer(instance.selected_options.all(), many=True).data
        return representation


class OrderListSerializer(serializers.ModelSerializer):

    user = UserSerializerModel()
    item = OrderItemSerializerRaw(many=True)

    class Meta:
        model = Order
        fields = ['id', 'quantity',  'user', 'item', 'total', 'Name', 'email', 'address']


class OrderSerializer(serializers.ModelSerializer):

    item = OrderItemSerializer(many=True)
    # user = UserSerializerModel()

    class Meta:
        model = Order
        fields = ['id', 'quantity', 'item', 'total', 'Name', 'email', 'address']


    def create(self, validated_data):
        
        request_data = self.context['request'].data
        loaded_order = request_data.get('item')
        user_id = request_data.get('user')
        # choices = request_data['choice']
        total_order = 0
        currentMenuItemId = None


        # Create the Order instance without the 'item' field
        user = User.objects.get(id=user_id)
        order = Order.objects.create(
            Name=validated_data['Name'],
            email=validated_data['email'],
            address=validated_data['address'],
            total=validated_data['total'],
            quantity=validated_data['quantity'],
            user=user
        )

        

        order_items = []
        for index,  data in enumerate(loaded_order):
            choice = data['choice'][index]
            print(index)
            print(choice)
            item_id = data['item']
            quantity = data['quantity']
            menu_item = MenuItem.objects.get(id=item_id)
            order_item = OrderItem.objects.create(quantity=quantity, item=menu_item)
            order.item.add(order_item.id)
            order_items.append(order_item)
            for key, value in choice.items():
                for option in value:
                    choice = Choices.objects.get(id=option['choiceId'])
                    choice = SelectedChoice.objects.create(
                        choice= choice.name,
                        option=option['title'],
                        price=option['amount'],
                        order_item=order_item
                    )

        
        total_order += int(request_data['total'])
        order.total = total_order
        order.save()

        # print(loaded_order)

        return order

class SelectedChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedChoice
        fields = ['choice', 'option', 'price']


class OrderedItemSerializer(serializers.ModelSerializer):
    selectedChoices = SelectedChoiceSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = ['item', 'selectedChoices', 'quantity']

    def create(self, validated_data):
        choices_data = validated_data.pop('selectedChoices')
        order_item = OrderItem.objects.create(**validated_data)
        for choice_data in choices_data:
            SelectedChoice.objects.create(order_item=order_item, **choice_data)
        return order_item






class PostOrderSerializer(serializers.ModelSerializer):
    item = OrderedItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['quantity', 'Name', 'user', 'item', 'email', 'address', 'total']

    def create(self, validated_data):
        items_data = validated_data.pop('item')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            self.fields['item'].create({'order': order, **item_data})
        return order



# serializer for authentication
class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()