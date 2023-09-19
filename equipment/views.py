from rest_framework import viewsets

from rest_framework.authentication import TokenAuthentication 
from rest_framework.permissions import IsAuthenticated

from core.models import (Equipment, Borrowing, History, User)
from equipment import serializers
from .serializers import CreateBorrowingSerializer, GetBorrowingSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EquipmentUserSerializer
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated]

# class CreateBorrowingViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.CreateBorrowingSerializer
#     queryset = Borrowing.objects.all()
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateBorrowingSerializer  # Use for POST requests
        # elif self.request.method in ['PUT', 'PATCH']:
        #     return UpdateBorrowingSerializer  # Use for PUT and PATCH requests
        return GetBorrowingSerializer  # Use for GET requests and other methods

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


# class BorrowingViewSet(viewsets.ModelViewSet):
#     serializer_class = BorrowingSerializer
#     queryset = Borrowing.objects.all()

#     def create(self, request, *args, **kwargs):
#         user = request.user  
#         equipment_id = request.data.get('equipment')
        
     
#         try:
#             equipment = Equipment.objects.get(id=equipment_id, stock_available__gt=0)
#         except Equipment.DoesNotExist:
#             return Response({"error": "Equipment not available for booking"}, status=status.HTTP_400_BAD_REQUEST)

#         # Calculate booking expiration date (h+1)
#         booking_expiration = datetime.now() + timedelta(hours=1)

#         # Create a new booking entry
#         booking = Borrowing.objects.create(
#             user=user,
#             equipment=equipment,
#             borrowing_until=booking_expiration,
#             status='Booking'
#         )

#         # Decrement stock_available
#         equipment.stock_available -= 1
#         equipment.save()

#         # Serialize and return the booking data
#         serializer = self.get_serializer(booking)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def update(self, request, *args, **kwargs):
#         # Extract data from the request
#         instance = self.get_object()
#         user = request.user  # Assuming you have authentication in place

#         # Check if the user is allowed to update (e.g., admin or authorized user)
#         if user.is_admin:
#             instance.status = 'Peminjaman'
#             instance.created_at = datetime.now()
#             instance.save()

#             # Increment stock_available upon borrowing
#             equipment = instance.equipment
#             equipment.stock_available += 1
#             equipment.save()

#             return Response({"message": "Equipment borrowed successfully"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Unauthorized to update the status"}, status=status.HTTP_403_FORBIDDEN)

#     def partial_update(self, request, *args, **kwargs):
#         # Extract data from the request
#         instance = self.get_object()
#         user = request.user  # Assuming you have authentication in place

#         # Check if the user is allowed to update (e.g., admin or authorized user)
#         if user.is_admin:
#             if 'status' in request.data and request.data['status'] == 'Pengembalian':
#                 # Handle equipment return
#                 instance.status = 'Pengembalian'
#                 instance.return_date = datetime.now()
#                 instance.save()

#                 # Increment stock_available upon return
#                 equipment = instance.equipment
#                 equipment.stock_available += 1
#                 equipment.save()

#                 return Response({"message": "Equipment returned successfully"}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "Invalid status for partial update"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error": "Unauthorized to update the status"}, status=status.HTTP_403_FORBIDDEN)


class HistoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HistorySerializer
    queryset = History.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class EquipmentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EquipmentSerializer
    queryset = Equipment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
