from rest_framework import serializers
from .models import WeekdayCommissionRule


class WeekdayCommissionRuleSerializer(serializers.ModelSerializer):
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)

    class Meta:
        model = WeekdayCommissionRule
        fields = [
            'id', 'weekday', 'weekday_display',
            'min_percentage', 'max_percentage'
        ]

    def validate(self, data):
        if data.get('min_percentage', 0) > data.get('max_percentage', 0):
            raise serializers.ValidationError(
                'O percentual mínimo não pode ser maior que o máximo.'
            )
        return data
