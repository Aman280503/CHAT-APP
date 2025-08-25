// Initialize Socket.io
const socket = io();

// DOM Elements
const joinScreen = document.getElementById('joinScreen');
const chatScreen = document.getElementById('chatScreen');
const joinForm = document.getElementById('joinForm');
const usernameInput = document.getElementById('usernameInput');
const messageForm = document.getElementById('messageForm');
const messageInput = document.getElementById('messageInput');
const messages = document.getElementById('messages');
const usersList = document.getElementById('usersList');
const currentUserSpan = document.getElementById('currentUser');
const leaveBtn = document.getElementById('leaveBtn');
const typingIndicator = document.getElementById('typingIndicator');

let username = '';
let typingTimer;

// Join form submission
joinForm.addEventListener('submit', (e) => {
    e.preventDefault();
    username = usernameInput.value.trim();

    if (username) {
        // Hide join screen and show chat screen
        joinScreen.style.display = 'none';
        chatScreen.style.display = 'block';

        // Set current user display
        currentUserSpan.textContent = username;

        // Emit join event
        socket.emit('join', username);

        // Focus on message input
        messageInput.focus();
    }
});

// Message form submission
messageForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = messageInput.value.trim();

    if (message) {
        // Emit chat message
        socket.emit('chatMessage', {
            username: username,
            message: message
        });

        // Clear input
        messageInput.value = '';

        // Stop typing indicator
        socket.emit('typing', { username: username, isTyping: false });
    }
});

// Typing indicator
messageInput.addEventListener('input', () => {
    socket.emit('typing', { username: username, isTyping: true });

    // Clear previous timer
    clearTimeout(typingTimer);

    // Set new timer to stop typing indicator
    typingTimer = setTimeout(() => {
        socket.emit('typing', { username: username, isTyping: false });
    }, 1000);
});

// Leave button
leaveBtn.addEventListener('click', () => {
    socket.disconnect();
    location.reload();
});

// Socket event listeners

// Receive chat messages
socket.on('message', (data) => {
    displayMessage(data, data.username === username ? 'own' : 'other');
});

// User joined notification
socket.on('userJoined', (data) => {
    displaySystemMessage(data.message);
});

// User left notification
socket.on('userLeft', (data) => {
    displaySystemMessage(data.message);
});

// Update users list
socket.on('updateUsersList', (users) => {
    updateUsersList(users);
});

// Typing indicator
socket.on('typing', (data) => {
    if (data.isTyping) {
        typingIndicator.textContent = `${data.username} is typing...`;
    } else {
        typingIndicator.textContent = '';
    }
});

// Functions

function displayMessage(data, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = data.message;

    const messageInfo = document.createElement('div');
    messageInfo.className = 'message-info';
    messageInfo.textContent = `${data.username} • ${formatTime(data.timestamp)}`;

    messageDiv.appendChild(messageContent);
    messageDiv.appendChild(messageInfo);

    messages.appendChild(messageDiv);
    scrollToBottom();
}

function displaySystemMessage(message) {
    const systemDiv = document.createElement('div');
    systemDiv.className = 'system-message';
    systemDiv.textContent = message;

    messages.appendChild(systemDiv);
    scrollToBottom();
}

function updateUsersList(users) {
    usersList.innerHTML = '';

    users.forEach(user => {
        const userDiv = document.createElement('div');
        userDiv.className = 'user-item';
        userDiv.innerHTML = `
            <i class="fas fa-user"></i> ${user.username}
            ${user.username === username ? '(You)' : ''}
        `;
        usersList.appendChild(userDiv);
    });
}

function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function scrollToBottom() {
    messages.scrollTop = messages.scrollHeight;
}

// Handle page refresh/close
window.addEventListener('beforeunload', () => {
    socket.disconnect();
});