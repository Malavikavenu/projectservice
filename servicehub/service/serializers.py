from rest_framework import serializers

from service.models import Customer,Work

from django.db.models import Sum


class WorkSerializer(serializers.ModelSerializer):

    customer_object=serializers.StringRelatedField(read_only=True)

    class Meta:
        model=Work
        fields="__all__"

        read_only_fields=[
                            "id","customer_object",
                            "created_date",
                            "updated_date",
                            "is_active"
                        ]
        


class CustomerSerializer(serializers.ModelSerializer):

    service_advisor=serializers.StringRelatedField(read_only=True)

    work_total=serializers.SerializerMethodField(read_only=True)
    
    works=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=Customer
        fields="__all__"

        read_only_fields=[
                        "id","service_advisor",
                        "created_date",
                        "updated_date",
                        "is_active"
                        ]

    def get_work_total(self,obj):

        total=Work.objects.filter(customer_object=obj).values("amount").aggregate(total=Sum("amount")).get("total")

        return total


    def get_works(self,obj):

        qs=Work.objects.filter(customer_object=obj)

        serializer_instance=WorkSerializer(qs,many=True)

        return serializer_instance.data