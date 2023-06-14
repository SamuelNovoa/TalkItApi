import json
import secrets

from django.http import JsonResponse

from talkItApp.models import User


def login(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'status': False}, status=404)

        data: dict = json.loads(request.body)

        email = data.get('email', None)
        password = data.get('password', None)

        if not email or not password:
            return JsonResponse({'status': False}, status=403)

        try:
            user = User.objects.get(email=email)
        except Exception:
            return JsonResponse({'status': False}, status=403)

        if user.password != password:
            return JsonResponse({'status': False}, status=403)

        user.apiCode = secrets.token_urlsafe()
        user.save()

        th_list = []
        for teacher in user.teacher_set.all():
            th_list.append({
                'teacher_id': teacher.id,
                'teacher_name': teacher.name,
                'teacher_gender': teacher.gender,
                'teacher_prompt': 'Personalidad por defecto.' if teacher.prompt is None else teacher.prompt
            })

        return JsonResponse({'status': True, 'username': user.username, 'apiCode': user.apiCode, 'teachers': th_list}, status=200)
    except Exception as e:
        return JsonResponse({'status': False}, status=500)


def logout(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'status': False}, status=404)

        data: dict = json.loads(request.body)

        api_code = data.get('apiCode', None)
        if not api_code:
            return JsonResponse({'status': False}, status=403)

        try:
            user = User.objects.get(apiCode=api_code)
        except Exception:
            return JsonResponse({'status': False}, status=403)

        user.apiCode = None
        user.save()

        return JsonResponse({'status': True}, status=200)
    except Exception as e:
        return JsonResponse({'status': False}, status=500)
