from django.shortcuts import render

from rest_framework import authentication,permissions,generics

from service.serializers import CustomerSerializer,WorkSerializer

from service.models import Customer,Work

from service.permissions import OwnerOnly

from django.db.models import Sum

from django.core.mail import send_mail

from twilio.rest import Client

import threading

account_sid = 'AC832faf1c977644073563d45567af6937'

auth_token = 'f9e6b8b3071ad12d8c6895759d189957'



def sent_text_message(vehicle_num,customer_name,total):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_='+18142472806',
    body=f"hai {customer_name} your vehicle {vehicle_num} service completed amount {total}",
    to='+918078116514'
)
    print(message.sid)


def sent_email_message(vehicle_num,cus_name,total):

    subject="vehicle service completion"

    message=f'your vehicle {vehicle_num} is ready to deliver service amount {total}'

    send_mail(subject,message,'malavikavenugopal99@gmail.com',['suchithravenugopal67@gmail.com'],fail_silently=False)



class CustomerListCreateView(generics.ListCreateAPIView):

    queryset=Customer.objects.all()

    serializer_class=CustomerSerializer

    model=Customer

    # authentication_classes=[authentication.TokenAuthentication]
    authentication_classes=[authentication.BasicAuthentication]


    permission_classes=[permissions.IsAdminUser]

    def perform_create(self, serializer):
        return serializer.save(service_advisor=self.request.user)
    


class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class=CustomerSerializer

    queryset=Customer.objects.all()

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAdminUser]

    def perform_update(self, serializer):

        # print("serializer instance",serializer.validated_data)

        work_status=serializer.validated_data.get("work_status")

        if work_status=="completed":

            print("sending email")

          

            vehicle_number=serializer.validated_data.get("vehicle_number")

          
            cus_name=serializer.validated_data.get("name")


            total=Work.objects.filter(customer_object__name=cus_name).values("amount").aggregate(total=Sum("amount")).get("total")

           
            
           



            # sent_text_message(vehicle_number,cus_name,total)

            # sent_email_message(vehicle_number,cus_name,total)

            message_thread=threading.Thread(target=sent_text_message,args=(vehicle_number,cus_name,total))

            email_thread=threading.Thread(target=sent_email_message,args=(vehicle_number,cus_name,total))

            message_thread.start()
            email_thread.start()

            



        serializer.save()
    



class WorkCreateView(generics.CreateAPIView):

    serializer_class=WorkSerializer

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAdminUser]

    def perform_create(self, serializer):
        id=self.kwargs.get("pk")

        cust_obj=Customer.objects.get(id=id)

        return serializer.save(customer_object=cust_obj)
    

class WorkUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class=WorkSerializer

    queryset=Work.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[OwnerOnly]
    


