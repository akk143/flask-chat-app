let socket;
let room;

function startConversation(userId) {
    fetch('/start_conversation/' + userId)
      .then(response => response.json())
      .then(data => {
          room = data.room;
          if (!socket) {
              socket = io();
              socket.on('chat_history', msgs => {
                  const messages = document.getElementById('messages');
                  messages.innerHTML = '';
                  msgs.forEach(msg => {
                      const li = document.createElement('li');
                      li.textContent = msg.sender + ': ' + msg.content;
                      messages.appendChild(li);
                  });
              });
              socket.on('receive_message', msg => {
                  const li = document.createElement('li');
                  li.textContent = msg.sender + ': ' + msg.content;
                  document.getElementById('messages').appendChild(li);
              });
          }
          socket.emit('join', { room: room });
          document.getElementById('chat-box').style.display = 'block';
      });
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form');
    const input = document.getElementById('input');
    form.addEventListener('submit', e => {
        e.preventDefault();
        if (input.value && room) {
            socket.emit('send_message', { room: room, content: input.value });
            input.value = '';
        }
    });
});