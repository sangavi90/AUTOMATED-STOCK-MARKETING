from rest_framework import serializers
from .models import *
from .models import pl

class CompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = company_name
        fields = ['company_name']

class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = options
        fields = ['ce', 'pe']

class ExpiryPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = options
        fields = ['ce', 'pe']        

class LegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leg
        fields = '__all__'


class StrategySerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = Strategy
        fields = ['user_id','strategy_id', 'strategy_name','status']

    

class LegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leg
        fields = '__all__'

def create(self, validated_data):
        strategy_instance = self.context.get('strategy_instance')
        leg_instance = Leg.objects.create(strategy_name=strategy_instance, **validated_data)
        return leg_instance


class SignInUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignInUser
        fields = '__all__'  # Add other fields as needed


class plSerializer(serializers.ModelSerializer):
    class Meta:
        model=pl
        fields = ['user_id', 'plid', 'company_name', 'trading_symbol', 'profit_loss', 'datetime']


class ThemesSerializer(serializers.ModelSerializer):
    class Meta:
        model=themes
        fields="__all__"