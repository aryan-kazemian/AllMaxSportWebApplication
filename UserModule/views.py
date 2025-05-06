from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import JSONParser
from UserModule.models import User
from UserModule.serializers import UserSerializer
from django.contrib.auth.decorators import login_required

@csrf_exempt
def user_api(request):
    user = request.user if request.user.is_authenticated else None

    if request.method == 'GET':
        if not user or (not user.is_staff and request.GET.get('id') != str(user.id)):
            return JsonResponse({'message': 'Permission denied'}, status=403)

        if request.GET.get('get_active_users_count') == 'true':
            if not user.is_staff:
                return JsonResponse({'message': 'Permission denied'}, status=403)
            active_users_count = User.objects.filter(is_active=True).count()
            return JsonResponse({'active_users_count': active_users_count})

        filters = {}
        if request.GET.get('id'):
            filters['id'] = request.GET.get('id')
        if request.GET.get('phone'):
            filters['phone'] = request.GET.get('phone')
        if request.GET.get('user_type'):
            filters['user_type'] = request.GET.get('user_type')
        if request.GET.get('first_name'):
            filters['first_name__icontains'] = request.GET.get('first_name')
        if request.GET.get('last_name'):
            filters['last_name__icontains'] = request.GET.get('last_name')
        if request.GET.get('email'):
            filters['email__icontains'] = request.GET.get('email')

        users = User.objects.filter(**filters)
        if not users.exists():
            return JsonResponse({'message': 'No user found with the given criteria'}, status=404)

        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)

        if data.get('action') == 'login':
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')

            try:
                user = User.objects.get(email=email) if email else User.objects.get(username=username)
                if check_password(password, user.password):
                    serializer = UserSerializer(user)
                    return JsonResponse(serializer.data, safe=False)
                else:
                    return JsonResponse({'message': 'Incorrect password'}, status=401)
            except User.DoesNotExist:
                return JsonResponse({'message': 'User not found'}, status=404)

        # Prevent privilege escalation
        for field in ['is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions']:
            if field in data:
                data[field] = False

        if 'password' in data:
            data['password'] = make_password(data['password'])

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'PATCH':
        if not user:
            return JsonResponse({'message': 'Authentication required'}, status=401)

        user_id = request.GET.get('id')
        if not user_id:
            return JsonResponse({'message': 'id is required in query'}, status=400)

        if not user.is_staff and str(user.id) != user_id:
            return JsonResponse({'message': 'Permission denied'}, status=403)

        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)

        data = JSONParser().parse(request)
        if 'password' in data:
            data['password'] = make_password(data['password'])

        # Prevent privilege escalation
        for field in ['is_staff', 'is_superuser', 'groups', 'user_permissions']:
            if field in data:
                del data[field]

        serializer = UserSerializer(target_user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if not user or not user.is_staff:
            return JsonResponse({'message': 'Only admin can delete users'}, status=403)

        user_id = request.GET.get('id')
        if not user_id:
            return JsonResponse({'message': 'id is required in query'}, status=400)

        try:
            target_user = User.objects.get(id=user_id)
            target_user.delete()
            return JsonResponse({'message': 'User deleted successfully'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)

    return JsonResponse({'message': 'Method not allowed'}, status=405)
