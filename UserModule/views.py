# views.py
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from UserModule.models import User
from UserModule.serializers import UserSerializer

@csrf_exempt
def user_api(request):
    if request.method == 'GET':
        if request.GET.get('get_active_users_count') == 'true':
            active_users_count = User.objects.filter(is_active=True).count()
            return JsonResponse({'active_users_count': active_users_count})

        user_id = request.GET.get('id')
        phone = request.GET.get('phone')
        user_type = request.GET.get('user_type')
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
        email = request.GET.get('email')

        filters = {}
        if user_id:
            filters['id'] = user_id
        if phone:
            filters['phone'] = phone
        if user_type:
            filters['user_type'] = user_type
        if first_name:
            filters['first_name__icontains'] = first_name
        if last_name:
            filters['last_name__icontains'] = last_name
        if email:
            filters['email__icontains'] = email

        users = User.objects.filter(**filters)
        if not users.exists():
            return JsonResponse({'message': 'No user found with the given criteria'}, status=404)

        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)


    elif request.method == 'POST':
        data = JSONParser().parse(request)
        if data.get('action') == 'login':
            email = data.get('email')
            password = data.get('password')
            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    serializer = UserSerializer(user)
                    return JsonResponse(serializer.data, safe=False)
                else:
                    return JsonResponse({'message': 'Incorrect password'}, status=401)
            except User.DoesNotExist:
                return JsonResponse({'message': 'No user with this email'}, status=404)
        else:
            if 'password' in data:
                data['password'] = make_password(data['password'])
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

    elif request.method == 'PATCH':
        user_id = request.GET.get('id')
        if not user_id:
            return JsonResponse({'message': 'id is required in query'}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)

        data = JSONParser().parse(request)
        if 'password' in data:
            data['password'] = make_password(data['password'])

        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user_id = request.GET.get('id')
        if not user_id:
            return JsonResponse({'message': 'id is required in query'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)

    return JsonResponse({'message': 'Method not allowed'}, status=405)
