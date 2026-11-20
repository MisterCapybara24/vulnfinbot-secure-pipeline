'use strict';
const form = document.querySelector('#chat-form');
const input = document.querySelector('#message');
const send = document.querySelector('#send');
const messages = document.querySelector('#messages');
function addMessage(text, role, meta) {
  const item = document.createElement('article'); item.className = `message ${role}`;
  const avatar = document.createElement('div'); avatar.className = 'avatar'; avatar.textContent = role === 'user' ? 'Вы' : 'Vf';
  const body = document.createElement('div');
  const author = document.createElement('span'); author.className = 'author'; author.textContent = role === 'user' ? 'ВАШ ВОПРОС' : 'MINI-VULNFINBOT';
  const textNode = document.createElement('p'); textNode.textContent = text;
  body.append(author, textNode);
  if (meta) { const small = document.createElement('small'); small.textContent = meta; body.append(small); }
  item.append(avatar, body); messages.append(item); messages.scrollTop = messages.scrollHeight;
}
input.addEventListener('input', () => { document.querySelector('#count').textContent = input.value.length; });
document.querySelectorAll('[data-prompt]').forEach(button => button.addEventListener('click', () => { input.value = button.dataset.prompt; input.dispatchEvent(new Event('input')); input.focus(); }));
fetch('/health').then(response => { if (!response.ok) throw new Error(); document.querySelector('#api-status').textContent = 'API доступен'; }).catch(() => { document.querySelector('#api-status').textContent = 'API недоступен'; });
form.addEventListener('submit', async event => {
  event.preventDefault(); const message = input.value.trim(); if (!message || send.disabled) return;
  addMessage(message, 'user'); send.disabled = true; send.textContent = 'Модель отвечает…';
  const controller = new AbortController(); const timer = setTimeout(() => controller.abort(), 140000);
  try {
    const response = await fetch('/api/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message}), signal:controller.signal});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Ошибка запроса');
    addMessage(data.response, 'assistant', `${data.model} · ${data.safety === 'blocked' ? 'Ответ заблокирован' : 'Ответ проверен'}${data.backend === 'mock' ? ' · MOCK, без вызова LLM' : ''}`);
    input.value = ''; input.dispatchEvent(new Event('input'));
  } catch (error) { addMessage(error.name === 'AbortError' ? 'Модель не успела ответить. Повторите запрос.' : error.message, 'assistant', 'Ответ не сгенерирован'); }
  finally { clearTimeout(timer); send.disabled = false; send.textContent = 'Отправить ↗'; input.focus(); }
});
