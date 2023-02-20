
from rest_framework import serializers
from .models import User
from datetime import date


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class AppointmentSerializers(serializers.Serializer):
    time_slot=[
        ('9','9'),
        ('12','12'),
        ('3','3')
    ]
    id = serializers.IntegerField(required=False)
    patientId=serializers.IntegerField()
    doctorId=serializers.IntegerField()
    patientName=serializers.CharField(max_length=40)
    doctorName=serializers.CharField(max_length=40)
    appointmentDate=serializers.DateField()
    #appointmentTime=serializers.TimeField()
    appointment_slot =serializers.ChoiceField(choices=time_slot,default='9' )
    #status=serializers.BooleanField(default=False)
    def validate(self, data):
        if data['appointmentDate'] < date.today():
            raise serializers.ValidationError("finish must occur after start")
        
        return data
