from django.urls import path
from transactions import transfer,payment_request
from bankaccounts.models import Account
app_name="transactions"
urlpatterns=[
    path("",transfer.search_user,name="search"),
    path("amount_transfer/<account_number>/",transfer.amount_transfer,name="amount_transfer"),
    path("amount_transfer_process/<account_number>/",transfer.amount_transfer_process,name="amount_transfer_process"),
    path('transfer_confirmation/<account_number>/<transaction_id>/',transfer.transfer_confirmation,name='transfer_confirmation'),
    path('transfer_success/<account_number>/<transaction_id>/',transfer.transfer_success,name='transfer_success'),
    path('transaction_detail/<transaction_id>/',transfer.transaction_detail,name='transaction_detail'),
    path('user_request_payment/',payment_request.user_request_payment_by_accnum,name='user_request_payment'),
    path('request_amount/<account_number>/',payment_request.request_amount,name='request_amount'),
    path('request_confirmation/<account_number>/<transaction_id>/',payment_request.request_confirmation,name='request_confirmation'),
    path('request_success/<account_number>/<transaction_id>/',payment_request.request_success,name='request_success'),
    path('transactions_list/',transfer.transactions_list,name='transactions_list'),
    path('send_confirmation/<account_number>/<transaction_id>/',payment_request.send_confirmation,name='send_confirmation'),
    path('send_complete/<account_number>/<transaction_id>/',payment_request.send_process,name='send_complete'),
    path('send_amount_complete/<account_number>/<transaction_id>/',payment_request.send_amount_complete,name='send_amount_complete'),
    # path('credit_card/<account_number>/<transaction_id>/',payment_request.credit_card,name='credit_card')
]