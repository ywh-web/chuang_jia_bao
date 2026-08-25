"""Knowledge-grounded assistant providers for the Chaoyun website."""

import json
import os
import re
from functools import lru_cache
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

KNOWLEDGE_PATH = Path(__file__).resolve().parent / 'knowledge' / 'chaoyun.md'
CHUNK_SIZE = 1200


@lru_cache(maxsize=1)
def knowledge_chunks():
    if not KNOWLEDGE_PATH.exists():
        return []
    text = KNOWLEDGE_PATH.read_text(encoding='utf-8')
    paragraphs = [part.strip() for part in re.split(r'\n\s*\n', text) if part.strip()]
    chunks, current = [], ''
    for paragraph in paragraphs:
        if len(current) + len(paragraph) + 2 > CHUNK_SIZE and current:
            chunks.append(current)
            current = ''
        current = f'{current}\n\n{paragraph}'.strip()
    if current:
        chunks.append(current)
    return chunks


def retrieve_context(question, limit=4):
    terms = {term.lower() for term in re.findall(r'[\w\u4e00-\u9fff]{2,}', question)}
    ranked = []
    for chunk in knowledge_chunks():
        lowered = chunk.lower()
        score = sum(lowered.count(term) for term in terms)
        if score:
            ranked.append((score, chunk))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in ranked[:limit]]


def _history_text(history):
    if not history:
        return '暂无历史对话。'
    return '\n'.join(f"{item['role']}: {item['content']}" for item in history)


def _prompt(question, context, history=None):
    context_text = '\n\n---\n\n'.join(context) or '知识库中暂时没有与问题直接匹配的内容。'
    history_text = _history_text(history or [])
    return (
        '你是潮韵商城的文化智能体。知识库有相关内容时必须优先依据知识库回答；'
        '知识库没有相关内容时，可以使用你的通用知识直接回答。'
        '涉及潮韵商城项目的具体事实、数据、人员或承诺时，知识库没有依据就不要猜测。'
        '使用简洁、亲切的中文。\n\n'
        f'知识库内容：\n{context_text}\n\n对话历史：\n{history_text}\n\n用户问题：{question}'
    )


def _post_json(url, payload, headers):
    request = Request(url, data=json.dumps(payload).encode('utf-8'), headers={**headers, 'Content-Type': 'application/json'}, method='POST')
    try:
        with urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as exc:
        detail = exc.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'Coze 请求失败（{exc.code}）：{detail[:300]}') from exc
    except URLError as exc:
        raise RuntimeError('无法连接 Coze 服务。') from exc


def _coze_text(data):
    if isinstance(data, dict):
        for key in ('answer', 'content', 'text', 'message'):
            if isinstance(data.get(key), str) and data[key].strip():
                return data[key].strip()
        for value in data.values():
            text = _coze_text(value)
            if text:
                return text
    if isinstance(data, list):
        for item in data:
            text = _coze_text(item)
            if text:
                return text
    if isinstance(data, str):
        try:
            return _coze_text(json.loads(data))
        except json.JSONDecodeError:
            return data.strip()
    return ''


def answer_with_coze(question, context, history):
    token = os.getenv('COZE_API_TOKEN', '').strip()
    bot_id = os.getenv('COZE_BOT_ID', '').strip()
    if not token or not bot_id:
        raise RuntimeError('COZE_API_TOKEN 或 COZE_BOT_ID 未配置。')
    base_url = os.getenv('COZE_BASE_URL', 'https://api.coze.cn').rstrip('/')
    payload = {
        'bot_id': bot_id,
        'user_id': 'chaoyun-web-visitor',
        'stream': False,
        'auto_save_history': True,
        'additional_messages': [
            {'role': 'user', 'content': _prompt(question, context, history), 'content_type': 'text'},
        ],
    }
    result = _post_json(f'{base_url}/v3/chat', payload, {'Authorization': f'Bearer {token}'})
    answer = _coze_text(result.get('data', result))
    if not answer:
        raise RuntimeError('Coze 尚未返回有效回答，请检查 Bot 是否已发布并开启 API。')
    return {'answer': answer, 'sources': ['Coze 智能体知识库'] if context else []}


def answer_with_deepseek(question, context, history):
    api_key = os.getenv('LLM_API_KEY', '').strip()
    if not api_key:
        raise RuntimeError('LLM_API_KEY 未配置。')
    from openai import OpenAI
    client = OpenAI(api_key=api_key, base_url=os.getenv('LLM_BASE_URL', 'https://api.deepseek.com').strip())
    response = client.chat.completions.create(
        model=os.getenv('LLM_MODEL', 'deepseek-v4-flash').strip(),
        temperature=0.2,
        max_tokens=700,
        messages=[
            {'role': 'system', 'content': _prompt('', context)},
            *history,
            {'role': 'user', 'content': question},
        ],
    )
    return {'answer': response.choices[0].message.content.strip(), 'sources': ['潮韵商城项目知识库'] if context else []}


def answer_question(question, history=None):
    context = retrieve_context(question)
    history = history or []
    provider = os.getenv('ASSISTANT_PROVIDER', 'deepseek').strip().lower()
    if provider == 'coze':
        return answer_with_coze(question, context, history)
    return answer_with_deepseek(question, context, history)



