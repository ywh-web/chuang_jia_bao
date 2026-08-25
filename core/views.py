import json

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import ContactInquiry
from .assistant_service import answer_question


def backend_home(request):
    return redirect('/admin/')


@csrf_exempt
@require_http_methods(['POST', 'OPTIONS'])
def contact_inquiry_create(request):
    if request.method == 'OPTIONS':
        return JsonResponse({}, status=204)

    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'message': '提交内容格式不正确。'}, status=400)

    name = str(payload.get('name', '')).strip()
    contact = str(payload.get('contact', '')).strip()
    cooperation_type = str(payload.get('type', '')).strip()
    message = str(payload.get('message', '')).strip()

    errors = {}
    if not name:
        errors['name'] = '请填写你的称呼。'
    if not contact:
        errors['contact'] = '请填写联系方式。'
    if cooperation_type not in ContactInquiry.CooperationType.values:
        errors['type'] = '请选择有效的合作方向。'
    if len(name) > 80:
        errors['name'] = '称呼不能超过 80 个字符。'
    if len(contact) > 160:
        errors['contact'] = '联系方式不能超过 160 个字符。'
    if len(message) > 2000:
        errors['message'] = '合作留言不能超过 2000 个字符。'
    if errors:
        return JsonResponse({'message': '请检查表单内容。', 'errors': errors}, status=400)

    inquiry = ContactInquiry.objects.create(
        name=name,
        contact=contact,
        cooperation_type=cooperation_type,
        message=message,
    )
    return JsonResponse({
        'message': '合作意向已记录，感谢你关注潮州嵌瓷数字化传承。',
        'id': inquiry.id,
    }, status=201)


@require_http_methods(['GET'])
def health_check(request):
    return JsonResponse({'status': 'ok'})
@csrf_exempt
@require_http_methods(['POST', 'OPTIONS'])
def assistant_chat(request):
    if request.method == 'OPTIONS':
        return JsonResponse({}, status=204)
    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'message': '问题格式不正确。'}, status=400)
    question = str(payload.get('question', '')).strip()
    if not question:
        return JsonResponse({'message': '请输入问题。'}, status=400)
    if len(question) > 1200:
        return JsonResponse({'message': '问题不能超过 1200 个字符。'}, status=400)
    try:
        result = answer_question(question)
    except RuntimeError as exc:
        return JsonResponse({'message': str(exc)}, status=503)
    except Exception:
        return JsonResponse({'message': '智能体暂时无法回答，请稍后再试。'}, status=502)
    return JsonResponse(result)

