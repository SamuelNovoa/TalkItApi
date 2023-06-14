import json

from django.http import JsonResponse

from talkItApp.models import User, Teacher


def teachers(request):
    try:
        if request.method == 'GET':
            api_code = request.GET.get('apiCode')

            if not api_code:
                return JsonResponse({'status': False}, status=401)

            try:
                user = User.objects.get(apiCode=api_code)
            except Exception:
                return JsonResponse({'status': False}, status=403)

            th_list = []
            for teacher in user.teacher_set.all():
                th_list.append({
                    'teacher_name': teacher.name,
                    'teacher_gender': teacher.gender,
                    'teacher_prompt': teacher.prompt
                })

            return JsonResponse({'status': True, 'teachers': th_list}, status=200)
        elif request.method == 'POST':
            data: dict = json.loads(request.body)
            api_code = data.get('apiCode', None)

            if not api_code:
                return JsonResponse({'status': False}, status=401)

            try:
                user = User.objects.get(apiCode=api_code)
            except Exception:
                return JsonResponse({'status': False}, status=403)

            teacher_name = data.get('teacher_name', None)
            teacher_gender = data.get('teacher_gender', None)
            teacher_prompt = data.get('teacher_prompt', None)

            if not teacher_name or not teacher_gender or not teacher_prompt:
                return JsonResponse({'status': False}, status=400)

            teacher = Teacher(name=teacher_name, gender=teacher_gender, prompt=teacher_prompt, user=user)
            teacher.save()
            return JsonResponse({'status': True}, status=200)
    except Exception as e:
        print(e)
        return JsonResponse({'status': False}, status=500)
