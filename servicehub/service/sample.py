# from twilio.rest import Client
# account_sid = 'AC832faf1c977644073563d45567af6937'
# auth_token = 'f9e6b8b3071ad12d8c6895759d189957'
# client = Client(account_sid, auth_token)
# message = client.messages.create(
#     from_='+18142472806',
#     body="message",
#     to='+918078116514'
# )
# print(message.sid)
import threading
import time

def sum_range(start,end):

    total=0

    for num in range(start,end):

        total=total+num
        time.sleep(.5) # to wait 1 mili sec

    print(total)


def product_range(start,end):

    product=1

    for num in range(start,end):

        product=product*num
        time.sleep(.5)

    print(product)


start_time=time.time()
sum_thread=threading.Thread(target=sum_range,args=(1,5))

product_thread=threading.Thread(target=product_range,args=(1,5))


sum_thread.start()
product_thread.start()

# sum_range(1,5)
# product_range(1,5)


end_time=time.time()

print("total time taken",end_time-start_time)