import json

from django.conf import settings
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Comment, ContactInquiry, UGCSubmission
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
    history = payload.get('history', [])
    if not isinstance(history, list):
        return JsonResponse({'message': '对话历史格式不正确。'}, status=400)
    normalized_history = []
    for item in history[-20:]:
        if not isinstance(item, dict):
            continue
        role = item.get('role')
        content = str(item.get('content', '')).strip()
        if role in {'user', 'assistant'} and content:
            normalized_history.append({'role': role, 'content': content[:2000]})
    try:
        result = answer_question(question, normalized_history)
    except RuntimeError as exc:
        return JsonResponse({'message': str(exc)}, status=503)
    except Exception:
        return JsonResponse({'message': '智能体暂时无法回答，请稍后再试。'}, status=502)
    return JsonResponse(result)



def _content_status(model):
    return model.Status.APPROVED if settings.DEBUG else model.Status.PENDING


def _comment_payload(comment):
    return {
        'id': comment.id,
        'pageKey': comment.page_key,
        'anchor': comment.anchor,
        'authorName': comment.author_name,
        'content': comment.content,
        'likeCount': comment.like_count,
        'createdAt': comment.created_at.isoformat(),
        'replies': [_comment_payload(reply) for reply in comment.replies.filter(status=Comment.Status.APPROVED)],
    }


@csrf_exempt
@require_http_methods(['GET', 'POST', 'OPTIONS'])
def comments_api(request):
    if request.method == 'OPTIONS':
        return JsonResponse({}, status=204)
    if request.method == 'GET':
        page_key = str(request.GET.get('page', '')).strip()[:80]
        anchor = str(request.GET.get('anchor', '')).strip()[:80]
        queryset = Comment.objects.filter(status=Comment.Status.APPROVED, parent__isnull=True)
        if page_key:
            queryset = queryset.filter(page_key=page_key)
        if anchor:
            queryset = queryset.filter(anchor=anchor)
        return JsonResponse({'items': [_comment_payload(comment) for comment in queryset[:60]]})

    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'message': '评论格式不正确。'}, status=400)
    page_key = str(payload.get('pageKey', '')).strip()
    anchor = str(payload.get('anchor', '')).strip()
    author_name = str(payload.get('authorName', '')).strip()
    content = str(payload.get('content', '')).strip()
    parent_id = payload.get('parentId')
    errors = {}
    if not page_key or len(page_key) > 80:
        errors['pageKey'] = '页面标识不正确。'
    if len(anchor) > 80:
        errors['anchor'] = '内容锚点不能超过 80 个字符。'
    if not author_name or len(author_name) > 80:
        errors['authorName'] = '昵称不能为空且不能超过 80 个字符。'
    if not content or len(content) > 1000:
        errors['content'] = '留言不能为空且不能超过 1000 个字符。'
    parent = None
    if parent_id:
        try:
            parent = Comment.objects.get(pk=int(parent_id), status=Comment.Status.APPROVED)
            if parent.page_key != page_key:
                errors['parentId'] = '回复对象不属于当前页面。'
        except (Comment.DoesNotExist, TypeError, ValueError):
            errors['parentId'] = '回复对象不存在。'
    if errors:
        return JsonResponse({'message': '请检查留言内容。', 'errors': errors}, status=400)
    comment = Comment.objects.create(
        page_key=page_key,
        anchor=anchor,
        author_name=author_name,
        content=content,
        parent=parent,
        status=_content_status(Comment),
    )
    return JsonResponse({'message': '留言已提交，感谢你的分享。', 'item': _comment_payload(comment)}, status=201)


@csrf_exempt
@require_http_methods(['POST', 'OPTIONS'])
def comment_like_api(request, pk):
    if request.method == 'OPTIONS':
        return JsonResponse({}, status=204)
    updated = Comment.objects.filter(pk=pk, status=Comment.Status.APPROVED).update(like_count=F('like_count') + 1)
    if not updated:
        return JsonResponse({'message': '评论不存在。'}, status=404)
    return JsonResponse({'likeCount': Comment.objects.values_list('like_count', flat=True).get(pk=pk)})


def _ugc_payload(request, item):
    return {
        'id': item.id,
        'title': item.title,
        'authorName': item.author_name,
        'contact': item.contact,
        'category': item.category,
        'categoryLabel': item.get_category_display(),
        'story': item.story,
        'imageUrl': request.build_absolute_uri(item.image.url) if item.image else '',
        'likeCount': item.like_count,
        'featured': item.featured,
        'createdAt': item.created_at.isoformat(),
    }


@csrf_exempt
@require_http_methods(['GET', 'POST', 'OPTIONS'])
def ugc_api(request):
    if request.method == 'OPTIONS':
        return JsonResponse({}, status=204)
    if request.method == 'GET':
        category = str(request.GET.get('category', '')).strip()
        queryset = UGCSubmission.objects.filter(status=UGCSubmission.Status.APPROVED)
        if category:
            queryset = queryset.filter(category=category)
        return JsonResponse({'items': [_ugc_payload(request, item) for item in queryset[:40]]})

    title = str(request.POST.get('title', '')).strip()
    author_name = str(request.POST.get('authorName', '')).strip()
    contact = str(request.POST.get('contact', '')).strip()
    category = str(request.POST.get('category', UGCSubmission.Category.STORY)).strip()
    story = str(request.POST.get('story', '')).strip()
    image = request.FILES.get('image')
    errors = {}
    if not title or len(title) > 120:
        errors['title'] = '标题不能为空且不能超过 120 个字符。'
    if not author_name or len(author_name) > 80:
        errors['authorName'] = '投稿人不能为空且不能超过 80 个字符。'
    if category not in UGCSubmission.Category.values:
        errors['category'] = '请选择有效的投稿类型。'
    if not story or len(story) > 3000:
        errors['story'] = '投稿内容不能为空且不能超过 3000 个字符。'
    if contact and len(contact) > 160:
        errors['contact'] = '联系方式不能超过 160 个字符。'
    if image:
        if image.size > 5 * 1024 * 1024:
            errors['image'] = '图片不能超过 5MB。'
        elif not (image.content_type or '').startswith('image/'):
            errors['image'] = '请上传图片文件。'
    if errors:
        return JsonResponse({'message': '请检查投稿内容。', 'errors': errors}, status=400)
    item = UGCSubmission.objects.create(
        title=title,
        author_name=author_name,
        contact=contact,
        category=category,
        story=story,
        image=image,
        status=_content_status(UGCSubmission),
    )
    return JsonResponse({'message': '投稿已提交，感谢你参与数字传家宝共创。', 'item': _ugc_payload(request, item)}, status=201)


@csrf_exempt
@require_http_methods(['POST', 'OPTIONS'])
def ugc_like_api(request, pk):
    if request.method == 'OPTIONS':
        return JsonResponse({}, status=204)
    updated = UGCSubmission.objects.filter(pk=pk, status=UGCSubmission.Status.APPROVED).update(like_count=F('like_count') + 1)
    if not updated:
        return JsonResponse({'message': '投稿不存在。'}, status=404)
    return JsonResponse({'likeCount': UGCSubmission.objects.values_list('like_count', flat=True).get(pk=pk)})

