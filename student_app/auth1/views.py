
import pika
import json

from django.http.response import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import ChangePasswordSerializer, MyTokenObtainPairSerializer, UpdateUserSerializer
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication

REQ_COURSE_HISTORY_CHANNEL = ''
REQ_COURSE_HISTORY_QUEUE = ''
REQ_COURSE_HISTORY_ROUTING_KEY = ''
RES_COURSE_HISTORY_CHANNEL = ''
RES_COURSE_HISTORY_QUEUE = ''


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

class ListCourseHistory(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        self.connection = None
        self._post_message('')
        queueResponse = ''
        while queueResponse == '':
            queueResponse = self._get_message()
        self._close_connection()
        return JsonResponse(json.loads(queueResponse), safe=False)


    def _get_message(self):
        if self.connection.is_closed:
            self._create_connection()
    
        channel = self.connection.channel()
        channel.queue_declare(queue='testqueue')
        method_frame, header_frame, body = channel.basic_get(queue = 'testqueue')        
        if not method_frame:
            return ''
        else:            
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            return body

    def _post_message(self, message):
        if not self.connection or self.connection.is_closed:
            self._create_connection()
    
        channel = self.connection.channel()
        channel.queue_declare(queue='testqueue1')
        channel.basic_publish('test',
                      'testKey1',
                       json.dumps({
                                    "username": "tamilselvan2",
                                    "first_name": "1",
                                    "last_name": "2",
                                    "email": "tamilselvan@ymail.com"
                                }),
                      pika.BasicProperties(content_type='text/plain',
                                           delivery_mode=1))

    def _create_connection(self):
        parameters = pika.ConnectionParameters()
        connection = pika.BlockingConnection(parameters)
        self.connection = connection
        return connection

    def _close_connection(self):
        self.connection.close()
        return True
