from django.shortcuts import render,redirect
from bankaccounts.models import Account,KYC
from transactions.models import Transaction
from django.db.models import Q
from django.contrib import messages

 

def user_request_payment_by_accnum(request):
    account=Account.objects.all()
    query=request.POST.get('account_number')
    print(query)
    if query:
        account=account.filter(
            Q(account_number=query)
        ).distinct()

    context={
        'account':account,
        'query':query,
    }
    return render(request,'payment_request/user_request_payment.html',context)

def request_amount(request,account_number):
    account=Account.objects.get(account_number=account_number)
    sender=request.user
    receiver=account.user
    sender_account=request.user.account
    receiver_account=account
    if request.method =='POST':
      amount=request.POST.get('amount-send')
      description=request.POST.get('description')
      if sender_account.account_balance > 0 and amount:
          new_transaction=Transaction.objects.create(
              description=description,
              user=request.user,
              amount=amount,
              sender_account=sender_account,
              sender=sender,
              receiver=receiver,
              receiver_account=receiver_account,
              status='request_sent',
              transaction_type='request',
          )
          new_transaction.save()
          transaction_id=new_transaction.transaction_id
          print(transaction_id)
          return redirect('transactions:request_confirmation',account.account_number,transaction_id)
      else:
         print('Insuffiecint balance')
       

    return render(request,'payment_request/request_amount.html',{'account':account})


def request_confirmation(request,account_number,transaction_id):
    try:
      account=Account.objects.get(account_number=account_number)
      transaction=Transaction.objects.get(transaction_id=transaction_id)
      kyc=KYC.objects.get(user=request.user)
      print(account.pin_number)
      if request.method == 'POST':
        pin_num=request.POST.get('pin-number')
        if transaction.amount<=account.account_balance:
          if account.pin_number==pin_num:
            transaction.status='request_sent'
            transaction.save()
            print(transaction.status)
            print('entered pinnumber',pin_num)
            return redirect('transactions:request_success',account.account_number,transaction_id)
          else:
            print('pin number is not matching')
          
        else:
           print('insuffcient balance')
      
    except:
        print('account doesnot exit')
    context={
       'account':account,
       'transaction':transaction,
       'kyc':kyc,
       }
    return render(request,'payment_request/request_confirmation.html',context)
   
def request_success(request,account_number,transaction_id):
    account=Account.objects.get(account_number=account_number)
    transaction=Transaction.objects.get(transaction_id=transaction_id)
    context={
       'account':account,
       'transaction':transaction,
    }
    return render(request,'payment_request/request_success.html',context)

def send_confirmation(request,account_number,transaction_id):
   account=Account.objects.get(account_number=account_number)
   transaction=Transaction.objects.get(transaction_id=transaction_id)
   if request.method=='POST':
      amount=request.POST.get('amount-send')
      description=request.POST.get('description')
      transaction.save()
      return redirect('transactions:send_complete',account.account_number,transaction.transaction_id)
      
   
   return render(request,'payment_request/send_confirmation.html',{'account':account,'transaction':transaction})
    

def send_process(request,account_number,transaction_id):
   account=Account.objects.get(account_number=account_number)
   transaction=Transaction.objects.get(transaction_id=transaction_id)
   
   sender=request.user
   sender_account=request.user.account

   if request.method=='POST':
      pin_num=request.POST.get('pin-number')
      print(pin_num)
      print(sender_account.pin_number)
      if pin_num==sender_account.pin_number:
         if sender_account.account_balance <=0 and sender_account.account_balance < transaction.amount :
            messages.warning(request,'Insufficient Amount.')

         else:
            sender_account.account_balance -= transaction.amount
            sender_account.save()
            
            account.account_balance += transaction.amount
            account.save()

            transaction.status='completed'
            transaction.save()

            messages.warning(request,f'Setteled to {account.user.kyc.full_name} was successfull')
            return redirect('transactions:send_amount_complete',account.account_number,transaction.transaction_id)

      else:
         messages.warning(request,'enter valid pin number')
   context={
         'account':account,
         'transaction':transaction,
         'sender':sender,
         'sender_account':sender_account,

      }
   return render(request,'payment_request/send_complete.html',context)


def send_amount_complete(request,account_number,transaction_id):
   account=Account.objects.get(account_number=account_number)
   transaction=Transaction.objects.get(transaction_id=transaction_id)

   sender=request.user
   sender_account=request.user.account

   context={
         'account':account,
         'transaction':transaction,
         'sender':sender,
         'sender_account':sender_account,

      }
   return render(request,'payment_request/send_amount_completed.html',context)