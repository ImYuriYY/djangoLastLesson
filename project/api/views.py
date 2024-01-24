from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def registration(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=201)
    return Response({'errors': {'code': 422, 'message': 'Validation error', 'errors': serializer.errors}}, status=422)



@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(email=serializer.validated_data['email'])
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=201)
    return Response({'errors': {'code': 422, 'message': 'Validation error', 'errors': serializer.errors}}, status=422)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response('Logout success')







@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def productsView(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'data': serializer.data})
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data})
        return Response({'errors': {'status': 422, 'message': 'Validation error', 'errors': serializer.errors}}, status=422)



@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def productView(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return Response('Not Found')
    
    if request.method == 'GET':
        products = Product.objects.get(pk=pk)
        serializer = ProductSerializer(products, many=True)
        return Response({'data': serializer.data})
    elif request.method == 'PUT':
        serializer = ProductSerializer(data=request.data, instance=product)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=201)
        return Response({'errors': {'status': 422, 'message': 'Validation error', 'errors': serializer.errors}}, status=422)
    elif request.method == 'PATCH':
        serializer = ProductSerializer(data=request.data, instance=product, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=201)
        return Response({'errors': {'status': 422, 'message': 'Validation error', 'errors': serializer.errors}}, status=422)
    elif request.method == 'DELETE':
        product.delete()
        return Response('Delete success')




@api_view(['GET'])
def cartInfo(request):
    cart = Cart.objects.filter(user=request.user)
    serializer = CartSerializer(cart, many=True)
    return Response({'data': serializer.data})


@api_view(['POST', 'DELETE'])
def cartChange(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return Response('Not Found')
    
    if request.method == 'POST':
        cart = Cart.objects.create(user=request.user)
        cart.product.add(product)
        return Response('Product added')
    elif request.method == 'DELETE':
        cart = Cart.objects.get(user=request.user)
        cart.product.remove(product)
        return Response('Product deleted')
    




