from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import UserSerializer, LoginSerializer, TranslatorSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from django.contrib.auth import authenticate
from googletrans import Translator, LANGUAGES
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Authenticate user
            user = authenticate(username=username, password=password)
            if user is not None:
                # User authenticated successfully
                # You may perform additional actions here, such as generating JWT token
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                # Authentication failed
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Serializer validation failed
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


    
@api_view(['POST'])
def translate(request):
    if request.method == 'POST':
        serializer = TranslatorSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data.get('text')
            target_language = serializer.validated_data.get('target_language')

            # Check if target_language is provided
            if not target_language:
                return Response({'error': 'Target language not provided'}, status=status.HTTP_400_BAD_REQUEST)

            # Translate text
            translator = Translator()
            try:
                translated_text = translator.translate(text, dest=target_language).text
                return Response({'translated_text': translated_text})
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': 'An error occurred during translation'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    



# render template for testing
def translate_form(request):
    return render(request, 'translate_form.html')



