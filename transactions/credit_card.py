from django.shortcuts import render,credit_card
from transactions.models import Creditcard



def credit_card_detail(request,number):
    credit_card=Creditcard.objects.get(number=number)
    return render(request,'account/credit_card_detail.html')

