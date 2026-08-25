/* 潮韵商城智能体入口：后续可将 answer() 替换为真实知识库接口。 */
(() => {
  const image = '/assets/ip_1_三视图.png'
  const quick = ['嵌瓷是什么？', '如何探索传家宝？', '我想合作']
  const replies = {
    '嵌瓷是什么？': '嵌瓷是潮州传统建筑装饰技艺，以彩瓷剪裁、拼嵌出人物、花鸟与瑞兽，寄托吉祥寓意。',
    '如何探索传家宝？': '你可以从“数字体验”开始，查看作品故事、工艺细节与数字凭证，再把喜欢的作品分享给家人。',
    '我想合作': '欢迎通过“合作咨询”提交需求，我们会根据校园研学、文旅数字化、家庭传承或纹样授权方向与你联系。',
  }
  const css = document.createElement('style')
  css.textContent = `.cy-agent-root{position:fixed;right:24px;bottom:24px;z-index:1200;font-family:inherit;color:#2b1a17}.cy-agent-launcher{display:flex;align-items:center;gap:10px;border:1px solid rgba(103,28,25,.2);border-radius:999px;padding:7px 14px 7px 7px;background:#f8f0e3;box-shadow:0 12px 32px rgba(50,22,16,.18);cursor:pointer;transition:.2s}.cy-agent-launcher:hover{transform:translateY(-2px)}.cy-agent-avatar{width:52px;height:52px;overflow:hidden;border-radius:50%;background:#f1d9ae;position:relative;flex:none}.cy-agent-avatar img{position:absolute;left:0;top:-7%;width:300%;height:116%;max-width:none;object-fit:cover;object-position:left center;mix-blend-mode:multiply}.cy-agent-launcher strong{font-size:14px;white-space:nowrap}.cy-agent-launcher small{display:block;margin-top:2px;color:#8b5c4d;font-size:11px}.cy-agent-panel{width:min(360px,calc(100vw - 32px));overflow:hidden;border:1px solid rgba(103,28,25,.16);border-radius:18px;background:#fbf6ed;box-shadow:0 20px 55px rgba(50,22,16,.24);animation:cy-agent-in .22s ease-out}@keyframes cy-agent-in{from{opacity:0;transform:translateY(10px) scale(.98)}to{opacity:1;transform:none}}.cy-agent-head{display:flex;align-items:center;gap:11px;padding:15px 16px;background:#671c19;color:#fff7e9}.cy-agent-head .cy-agent-avatar{width:45px;height:45px}.cy-agent-head strong{font-size:16px}.cy-agent-head small{display:block;margin-top:3px;color:#eac9a8;font-size:11px}.cy-agent-close{margin-left:auto;border:0;background:transparent;color:inherit;font-size:22px;cursor:pointer}.cy-agent-body{padding:16px}.cy-agent-message{display:flex;gap:9px;align-items:flex-start}.cy-agent-message .cy-agent-avatar{width:30px;height:30px}.cy-agent-bubble{max-width:270px;padding:10px 12px;border-radius:4px 13px 13px 13px;background:#efe1cc;color:#50352b;font-size:13px;line-height:1.6}.cy-agent-suggestions{display:flex;flex-wrap:wrap;gap:7px;margin:14px 0 13px 39px}.cy-agent-suggestions button{border:1px solid #d9b88d;border-radius:999px;padding:7px 10px;background:#fffaf2;color:#7a321f;cursor:pointer;font:inherit;font-size:12px}.cy-agent-form{display:flex;gap:7px;padding-top:10px;border-top:1px solid #ead8c1}.cy-agent-form input{min-width:0;flex:1;border:1px solid #d9c3aa;border-radius:8px;padding:10px;background:#fffdf9;color:#2b1a17;outline:none;font:inherit;font-size:13px}.cy-agent-form button{border:0;border-radius:8px;padding:0 13px;background:#9e2e25;color:white;cursor:pointer;font:inherit;font-size:13px}@media(max-width:600px){.cy-agent-root{right:14px;bottom:14px}.cy-agent-launcher{padding-right:11px}.cy-agent-avatar{width:46px;height:46px}.cy-agent-panel{width:calc(100vw - 28px)}.cy-agent-body{padding:13px}}`
  document.head.appendChild(css)
  const avatar = () => `<span class="cy-agent-avatar"><img src="${image}" alt="潮韵智能体形象"></span>`
  const root = document.createElement('div'); root.className = 'cy-agent-root'; document.body.appendChild(root)
  const launcher = () => { root.innerHTML = `<button class="cy-agent-launcher" type="button" aria-label="打开潮韵智能体">${avatar()}<span><strong>潮韵小助手</strong><small>点击和我聊聊嵌瓷</small></span></button>`; root.querySelector('button').onclick = panel }
  const panel = () => { root.innerHTML = `<section class="cy-agent-panel" aria-label="潮韵智能体"><header class="cy-agent-head">${avatar()}<span><strong>潮韵小助手</strong><small>一起认识潮州嵌瓷</small></span><button class="cy-agent-close" type="button" aria-label="关闭">×</button></header><div class="cy-agent-body"><div class="cy-agent-message">${avatar()}<div class="cy-agent-bubble">你好，我是潮韵商城的小助手。想了解嵌瓷、数字传承或合作方式吗？</div></div><div class="cy-agent-suggestions">${quick.map((q) => `<button type="button" data-q="${q}">${q}</button>`).join('')}</div><form class="cy-agent-form"><input aria-label="输入问题" placeholder="输入你想了解的内容…" maxlength="120"><button type="submit">发送</button></form></div></section>`; root.querySelector('.cy-agent-close').onclick = launcher; root.querySelectorAll('[data-q]').forEach((b) => b.onclick = () => answer(b.dataset.q)); root.querySelector('form').onsubmit = (e) => { e.preventDefault(); const i=e.currentTarget.querySelector('input'); answer(i.value.trim()); i.value='' } }
  const answer = async (q) => {
    const bubble = root.querySelector('.cy-agent-bubble')
    if (!bubble) return
    if (!q) { bubble.textContent = '可以点击上面的快捷问题，或输入你想了解的内容。'; return }
    bubble.textContent = '正在查阅潮韵商城知识库…'
    try {
      const base = window.__CHAoyun_API_BASE__ || 'http://127.0.0.1:8000'
      const response = await fetch(base + '/api/assistant/chat/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question: q }) })
      const data = await response.json()
      if (!response.ok) throw new Error(data.message || 'request failed')
      bubble.textContent = data.answer
    } catch (error) {
      bubble.textContent = error.message || '暂时无法连接后端，请检查 Django 服务。'
    }
  }
  launcher()
})()



