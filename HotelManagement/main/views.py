from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Offer, Room, UserProfile, Feedback, Booking
import logging
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)

User = get_user_model()

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'email': user.email})

@csrf_exempt
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        token = Token.objects.create(user=user)
        return JsonResponse({'token': token.key})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@api_view(['GET'])
def fetch_offers(request):
    offers = Offer.objects.all()
    data = [{'id': offer.id, 'title': offer.title, 'location': offer.location, 'price': str(offer.price), 
             'discount': offer.discount, 'beds': offer.beds, 'bathtub': offer.bathtub, 
             'wifi': offer.wifi, 'shuttle': offer.shuttle, 'image': offer.image.url if offer.image else None} 
            for offer in offers]
    return JsonResponse(data, safe=False)

@api_view(['GET'])
def fetch_rooms(request):
    rooms = Room.objects.all()
    data = [{'id': room.id, 'destTitle': room.destTitle, 'desc': room.desc, 'price': str(room.price), 
             'beds': room.beds, 'bathtub': room.bathtub, 'wifi': room.wifi, 
             'shuttle': room.shuttle, 'image': room.image.url if room.image else None} 
            for room in rooms]
    return JsonResponse(data, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    user = request.user
    profile = UserProfile.objects.filter(user=user).first()
    data = {
        'username': user.username,
        'email': user.email,
        'profileImage': profile.profile_image.url if profile and profile.profile_image else None
    }
    return JsonResponse(data)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = request.data
    user.first_name = data.get('fullName').split()[0]
    user.last_name = ' '.join(data.get('fullName').split()[1:])
    user.email = data.get('email')

    profile, created = UserProfile.objects.get_or_create(user=user)
    if 'profileImage' in data:
        profile.profile_image = data['profileImage']
        profile.save()

    if 'password' in data and data['password']:
        user.set_password(data['password'])
        user.save()

    return JsonResponse({'message': 'Profile updated successfully'})

@csrf_exempt
@api_view(['POST'])
def password_reset(request):
    # Placeholder for password reset implementation
    return JsonResponse({'message': 'Password reset functionality not implemented yet'})

@csrf_exempt
@api_view(['POST'])
def password_reset_confirm(request):
    # Placeholder for password reset confirmation implementation
    return JsonResponse({'message': 'Password reset confirmation not implemented yet'})

@csrf_exempt
@api_view(['GET'])
def search_rooms(request):
    # Placeholder for room search implementation
    return JsonResponse({'message': 'Room search functionality not implemented yet'})

@csrf_exempt
@api_view(['GET'])
def view_rooms(request):
    # Placeholder for room view implementation
    return JsonResponse({'message': 'Room view functionality not implemented yet'})

@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def book_room(request):
    if request.method == 'POST':
        data = request.data
        user = request.user
        room_id = data.get('room_id')
        check_in = data.get('check_in')
        check_out = data.get('check_out')

        # Ensure room exists or return a 404 Not Found response
        room = get_object_or_404(Room, id=room_id)

        # Assuming basic implementation without additional checks

        booking = Booking.objects.create(user=user, room=room, check_in=check_in, check_out=check_out)
        booking.save()

        return JsonResponse({'message': 'Room booked successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_booked_rooms(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)
    data = [{'id': booking.id, 'room': booking.room.destTitle, 'check_in': booking.check_in, 
             'check_out': booking.check_out, 'approved': booking.approved} 
            for booking in bookings]
    return JsonResponse(data, safe=False)

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_booked_room(request, booking_id):
    if request.method == 'DELETE':
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            booking.delete()
            return JsonResponse({'message': 'Booking canceled successfully'})
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@api_view(['POST'])
def submit_feedback(request):
    if request.method == 'POST':
        data = request.data
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        feedback = Feedback.objects.create(name=name, email=email, message=message)
        feedback.save()

        return JsonResponse({'message': 'Feedback submitted successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
