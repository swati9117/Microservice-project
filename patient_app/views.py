from ast import Delete
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer,AppointmentSerializers
from .models import User
import jwt, datetime
from rest_framework import status
import requests

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        userDetails = {
            'patientId' : user.id,
            'patientName' : user.name,
            'email' : user.email,
            

        }
      
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'userDetails':userDetails
            
        }
        return response

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

class AppointmentAPIView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()

        return Response(self.format_appointment(user.id))

    def format_appointment(self,patient):
        appointment = requests.get('http://127.0.0.1:8001/Patient/%d/appointment/'%patient).json()
        
        return{
            'id':patient,
            'appointment':appointment

        }
    
    def post(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        serializer = AppointmentSerializers(data=request.data)
        if request.data['patientId']!=str(payload['id']) :
            return Response({'msg':'You cannot booked appointement for another user id'})
        if serializer.is_valid(raise_exception=True):
            r = requests.post('http://127.0.0.1:8001/appointment_details/',serializer.data)
            print(r.json)
            return Response(r.json())
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    


class AppointmentUpdateAPIView(APIView):
    def put(self, request,slug):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        serializer = AppointmentSerializers(data=request.data)
        if request.data['patientId']!= payload['id']:
            return Response({'msg':'You cannot update appointement for another user id'})
        if serializer.is_valid(raise_exception=True):
            print(serializer.data)

            r = requests.put('http://127.0.0.1:8001/update_appointment_details/%d/'%slug,serializer.data)
            
            return Response(r.json())
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# class AppointmentDeleteAPIView(APIView):
    def delete(self, request,slug):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print(payload['id'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        r = requests.delete('http://127.0.0.1:8001/update_appointment_details/%d/'%slug)
            
        return Response(r.json())
        

    
