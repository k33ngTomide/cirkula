from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from user.models import CirkulaUser
from user.serializers import CirkulaUserSerializer
from wallet.models import Wallet

from wallet import views as wallet_views


class CirkulaUserViewSet(ModelViewSet):
    queryset = CirkulaUser.objects.all()
    serializer_class = CirkulaUserSerializer
    permission_classes = [IsAuthenticated]


def deposit(deposit_request) -> JsonResponse:
    wallet = get_user_wallet(deposit_request)
    wallet.deposit(deposit_request.amount)

    return JsonResponse({'message': "Deposit Successful"}, status=200)


def withdraw(withdraw_request) -> JsonResponse:
    wallet = get_user_wallet(withdraw_request)
    wallet.withdraw(withdraw_request.amount, withdraw_request.pin)

    return JsonResponse({'message': "Withdraw Successful"}, status=200)


def get_user_wallet(request) -> Wallet:
    user = CirkulaUser.objects.get(id=request.user.id)
    wallet = Wallet.objects.get(user=user)
    return wallet


def transfer(transfer_request) -> HttpResponse:
    wallet = get_user_wallet(transfer_request)
    receiver_wallet = Wallet.objects.get(user=transfer_request.receiver)
    wallet.transfer(receiver_wallet, transfer_request.amount, transfer_request.pin)

    return HttpResponse("Transfer Successful")


def get_user_details(request, username):
    try:
        user = CirkulaUser.objects.get(username=username)
        return JsonResponse({'username': user.username, 'email': user.email})
    except CirkulaUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


def find_user_wallet(get_wallet_request) -> JsonResponse:
    found_wallet = wallet_views.find_wallet(get_wallet_request.username)
    if not found_wallet:
        return JsonResponse({'error': 'user wallet not found'}, status=404)
    return JsonResponse({found_wallet}, status=200)
