from rest_framework import serializers 
from core.models import (Equipment, History, Borrowing, User)


class EquipmentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id','name', 'email', 'role', 'phone_number']

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Equipment
        fields = '__all__'
        read_only_fields = ['id']
        
    def create(self, validated_data):
        equipment = Equipment.objects.create(**validated_data)
        return equipment 

    def update(self, instance, validated_data):
        for attr, value, in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class Equipments(serializers.ModelSerializer):
    class Meta: 
        model = Equipment
        fields = ['name', 'description', 'stock_available', 'image']

class GetBorrowingSerializer(serializers.ModelSerializer):
    user = EquipmentUserSerializer()
    equipment = Equipments()
    created_by = EquipmentUserSerializer()

    class Meta:
        model = Borrowing
        fields = '__all__'
        read_only_fields = ['id']

class CreateBorrowingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    equipment = serializers.PrimaryKeyRelatedField(queryset=Equipment.objects.all(), write_only=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Borrowing
        fields = '__all__'
    

class HistorySerializer(serializers.ModelSerializer):
    borrowings = GetBorrowingSerializer()
    created_by = EquipmentUserSerializer()
    
    class Meta:
        model = History
        fields = '__all__'
        # read_only_fields = ['id']

