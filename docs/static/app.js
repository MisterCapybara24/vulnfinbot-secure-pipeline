'use strict';
const form = document.querySelector('#chat-form');
const input = document.querySelector('#message');
const messages = document.querySelector('#messages');
const count = document.querySelector('#count');
function addMessage(text, role) {
  const article = document.createElement('article'); article.className = `message ${role}`;
  const avatar = document.createElement('div'); avatar.className = 'avatar'; avatar.textContent = role === 'user' ? 'Вы' : '✦';
  const body = document.createElement('div');
  const author = document.createElement('span'); author.className = 'author'; author.textContent = role === 'user' ? 'ВАШ ВОПРОС' : 'ГОТОВЫЙ ДЕМОПРИМЕР · НЕ AI';
  const p = document.createElement('p'); p.textContent = text;
  body.append(author, p); article.append(avatar, body); messages.append(article); messages.scrollTop = messages.scrollHeight;
}
input.addEventListener('input', () => { count.textContent = input.value.length; });
document.querySelectorAll('[data-prompt]').forEach(button => button.addEventListener('click', () => {
  input.value = button.dataset.prompt; input.dispatchEvent(new Event('input')); input.focus();
}));
form.addEventListener('submit', event => {
  event.preventDefault(); const message = input.value.trim(); if (!message) return;
  addMessage(message, 'user');
  let reply = 'Это статическая демонстрация без AI. Доступны готовые примеры о бюджете и финансовой подушке — выберите подсказку над полем. Полная Flask/Ollama-версия и инструкции запуска доступны по ссылке GitHub.';
  if (/подушк|резерв|savings|emergency/i.test(message)) reply = 'Готовый пример: при вымышленных обязательных расходах 150 000 ₸ в месяц резерв на 3 месяца составит 450 000 ₸. Если откладывать 30 000 ₸ в месяц, без учёта процентов понадобится 15 месяцев. Это учебный пример, не персональная рекомендация.';
  else if (/бюджет|budget/i.test(message)) reply = 'Готовый пример для вымышленного дохода 300 000 ₸: обязательные расходы — 150 000 ₸, накопления — 60 000 ₸, остальные расходы — 90 000 ₸. Итого 300 000 ₸. Суммы фиксированы и не рассчитываются из вашего сообщения.';
  addMessage(reply, 'assistant'); input.value = ''; count.textContent = '0'; input.focus();
});
