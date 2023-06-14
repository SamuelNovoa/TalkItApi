import json

from django.http import JsonResponse

from talkItApp.models import User, Teacher
from talkItApp.services.inference_service import InferenceService


def do_response(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'status': False}, status=404)

        data: dict = json.loads(request.body)

        api_code = data.get('apiCode', None)
        teacher_name = data.get('teacher_name', None)
        question = data.get('question', None)

        if not api_code or not teacher_name:
            return JsonResponse({'status': False}, status=403)

        try:
            user = User.objects.get(apiCode=api_code)
            teacher = Teacher.objects.get(name=teacher_name)
        except Exception as e:
            return JsonResponse({'status': False}, status=403)

        answer_voice, answer_text = InferenceService.get_instance().get_response(question, user, teacher)
        return JsonResponse({'status': True, 'answer_voice': answer_voice, 'answer_text': answer_text}, status=200)
    except Exception as e:
        print(e)
        return JsonResponse({'status': False}, status=500)
