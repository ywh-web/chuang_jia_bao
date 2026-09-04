/* 潮韵商城智能体入口：支持连续对话与本地会话记录。 */
(() => {
  const image = '/assets/ip_1_三视图.png'
  const quick = ['嵌瓷是什么？', '如何探索传家宝？', '我想合作']
  const storageKey = 'chaoyun-agent-history-v1'
  const greeting = '你好，我是潮韵商城的小助手。想了解嵌瓷、数字传承或合作方式吗？'
  const css = document.createElement('style')
  css.textContent = '.cy-agent-root{position:fixed;right:24px;bottom:24px;z-index:1200;font-family:inherit;color:#2b1a17}.cy-agent-launcher{display:flex;align-items:center;gap:10px;border:1px solid rgba(103,28,25,.2);border-radius:999px;padding:7px 14px 7px 7px;background:#f8f0e3;box-shadow:0 12px 32px rgba(50,22,16,.18);cursor:pointer;transition:.2s}.cy-agent-launcher:hover{transform:translateY(-2px)}.cy-agent-avatar{width:52px;height:52px;overflow:hidden;border-radius:50%;background:#f1d9ae;position:relative;flex:none}.cy-agent-avatar img{position:absolute;left:0;top:-7%;width:300%;height:116%;max-width:none;object-fit:cover;object-position:left center;mix-blend-mode:multiply}.cy-agent-launcher strong{font-size:14px;white-space:nowrap}.cy-agent-launcher small{display:block;margin-top:2px;color:#8b5c4d;font-size:11px}.cy-agent-panel{width:min(360px,calc(100vw - 32px));overflow:hidden;border:1px solid rgba(103,28,25,.16);border-radius:18px;background:#fbf6ed;box-shadow:0 20px 55px rgba(50,22,16,.24);animation:cy-agent-in .22s ease-out}@keyframes cy-agent-in{from{opacity:0;transform:translateY(10px) scale(.98)}to{opacity:1;transform:none}}.cy-agent-head{display:flex;align-items:center;gap:11px;padding:15px 16px;background:#671c19;color:#fff7e9}.cy-agent-head .cy-agent-avatar{width:45px;height:45px}.cy-agent-head strong{font-size:16px}.cy-agent-head small{display:block;margin-top:3px;color:#eac9a8;font-size:11px}.cy-agent-close,.cy-agent-clear{border:0;background:transparent;color:inherit;cursor:pointer}.cy-agent-clear{margin-left:auto;font-size:11px;opacity:.8}.cy-agent-close{font-size:22px;margin-left:4px}.cy-agent-body{padding:16px}.cy-agent-messages{display:flex;flex-direction:column;gap:10px;max-height:310px;overflow:auto;padding-right:2px}.cy-agent-message{display:flex;gap:9px;align-items:flex-start}.cy-agent-message-user{justify-content:flex-end}.cy-agent-message .cy-agent-avatar{width:30px;height:30px}.cy-agent-bubble{max-width:270px;padding:10px 12px;border-radius:4px 13px 13px 13px;background:#efe1cc;color:#50352b;font-size:13px;line-height:1.6;white-space:pre-wrap;word-break:break-word}.cy-agent-message-user .cy-agent-bubble{border-radius:13px 4px 13px 13px;background:#9e2e25;color:#fff7e9}.cy-agent-suggestions{display:flex;flex-wrap:wrap;gap:7px;margin:14px 0 13px 39px}.cy-agent-suggestions button{border:1px solid #d9b88d;border-radius:999px;padding:7px 10px;background:#fffaf2;color:#7a321f;cursor:pointer;font:inherit;font-size:12px}.cy-agent-form{display:flex;gap:7px;padding-top:10px;border-top:1px solid #ead8c1}.cy-agent-form input{min-width:0;flex:1;border:1px solid #d9c3aa;border-radius:8px;padding:10px;background:#fffdf9;color:#2b1a17;outline:none;font:inherit;font-size:13px}.cy-agent-form button{border:0;border-radius:8px;padding:0 13px;background:#9e2e25;color:white;cursor:pointer;font:inherit;font-size:13px}.cy-agent-form button:disabled{opacity:.55;cursor:wait}@media(max-width:600px){.cy-agent-root{right:14px;bottom:14px}.cy-agent-launcher{padding-right:11px}.cy-agent-avatar{width:46px;height:46px}.cy-agent-panel{width:calc(100vw - 28px)}.cy-agent-body{padding:13px}}'
  document.head.appendChild(css)

  const avatar = () => '<span class="cy-agent-avatar"><img src="' + image + '" alt="潮韵智能体形象"></span>'
  const root = document.createElement('div')
  root.className = 'cy-agent-root'
  document.body.appendChild(root)
  let history = loadHistory()

  function loadHistory() {
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey) || '[]')
      if (!Array.isArray(saved)) return []
      return saved.filter((item) => item && ['user', 'assistant'].includes(item.role) && typeof item.content === 'string').slice(-20)
    } catch {
      return []
    }
  }

  function saveHistory() {
    history = history.slice(-20)
    localStorage.setItem(storageKey, JSON.stringify(history))
  }

  function appendMessage(role, text) {
    const list = root.querySelector('.cy-agent-messages')
    if (!list) return null
    const row = document.createElement('div')
    row.className = 'cy-agent-message cy-agent-message-' + role
    if (role === 'assistant') row.innerHTML = avatar()
    const bubble = document.createElement('div')
    bubble.className = 'cy-agent-bubble'
    bubble.textContent = text
    row.appendChild(bubble)
    list.appendChild(row)
    list.scrollTop = list.scrollHeight
    return bubble
  }

  function renderMessages() {
    const list = root.querySelector('.cy-agent-messages')
    if (!list) return
    list.innerHTML = ''
    appendMessage('assistant', greeting)
    history.forEach((item) => appendMessage(item.role, item.content))
  }

  const launcher = () => {
    root.innerHTML = '<button class="cy-agent-launcher" type="button" aria-label="打开潮韵智能体">' + avatar() + '<span><strong>潮韵小助手</strong><small>点击和我聊聊嵌瓷</small></span></button>'
    root.querySelector('button').onclick = panel
  }

  const panel = () => {
    root.innerHTML = '<section class="cy-agent-panel" aria-label="潮韵智能体"><header class="cy-agent-head">' + avatar() + '<span><strong>潮韵小助手</strong><small>一起认识潮州嵌瓷</small></span><button class="cy-agent-clear" type="button">清空记录</button><button class="cy-agent-close" type="button" aria-label="关闭">×</button></header><div class="cy-agent-body"><div class="cy-agent-messages"></div><div class="cy-agent-suggestions">' + quick.map((q) => '<button type="button" data-q="' + q + '">' + q + '</button>').join('') + '</div><form class="cy-agent-form"><input aria-label="输入问题" placeholder="输入你想了解的内容…" maxlength="120"><button type="submit">发送</button></form></div></section>'
    renderMessages()
    root.querySelector('.cy-agent-close').onclick = launcher
    root.querySelector('.cy-agent-clear').onclick = () => { history = []; localStorage.removeItem(storageKey); renderMessages() }
    root.querySelectorAll('[data-q]').forEach((button) => { button.onclick = () => answer(button.dataset.q) })
    root.querySelector('form').onsubmit = (event) => { event.preventDefault(); const input = event.currentTarget.querySelector('input'); answer(input.value.trim()); input.value = '' }
  }

  const answer = async (question) => {
    const q = question.trim()
    if (!q) return
    const previousHistory = history.slice(-20)
    history.push({ role: 'user', content: q })
    saveHistory()
    appendMessage('user', q)
    const pending = appendMessage('assistant', '正在查阅潮韵商城知识库…')
    const form = root.querySelector('.cy-agent-form')
    const submit = form ? form.querySelector('button') : null
    if (submit) submit.disabled = true
    try {
      const configuredBase = window.__CHAoyun_API_BASE__ || 'http://127.0.0.1:8000/api'
      const base = configuredBase.replace(/\/+$/, '')
      const endpoint = /\/api$/i.test(base) ? base + '/assistant/chat/' : base + '/api/assistant/chat/'
      const response = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question: q, history: previousHistory }) })
      const contentType = response.headers.get('content-type') || ''
      if (!contentType.includes('application/json')) throw new Error(`助手接口暂时不可用（${response.status}），请检查后端服务地址。`)
      const data = await response.json()
      if (!response.ok) throw new Error(data.message || 'request failed')
      pending.textContent = data.answer
      history.push({ role: 'assistant', content: data.answer })
      saveHistory()
    } catch (error) {
      const message = error.message || '暂时无法连接后端，请检查 Django 服务。'
      pending.textContent = message
      history.push({ role: 'assistant', content: message })
      saveHistory()
    } finally {
      if (submit) submit.disabled = false
    }
  }

  launcher()
})()