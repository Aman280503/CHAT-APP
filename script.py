# Create project structure and files for Chat App

import os

# Create project directory structure
project_files = {
    'package.json': '''{
  "name": "realtime-chat-app",
  "version": "1.0.0",
  "description": "Real-time chat application using Node.js, Express, and Socket.io",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "socket.io": "^4.7.2"
  },
  "devDependencies": {
    "nodemon": "^3.0.1"
  },
  "keywords": ["chat", "socket.io", "nodejs", "express", "realtime"],
  "author": "Aman Agrawal",
  "license": "MIT"
}''',

    'server.js': '''const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

const PORT = process.env.PORT || 3000;

// Serve static files from public directory
app.use(express.static(path.join(__dirname, 'public')));

// Store connected users
let users = [];

// Socket.io connection handling
io.on('connection', (socket) => {
    console.log('A user connected:', socket.id);

    // Handle user joining
    socket.on('join', (username) => {
        const user = {
            id: socket.id,
            username: username,
            joinTime: new Date()
        };
        
        users.push(user);
        socket.username = username;
        
        // Notify all users about new user
        socket.broadcast.emit('userJoined', {
            username: username,
            message: `${username} joined the chat`,
            timestamp: new Date()
        });
        
        // Send current users list to the new user
        socket.emit('usersList', users);
        
        // Send users list to all clients
        io.emit('updateUsersList', users);
        
        console.log(`${username} joined the chat`);
    });

    // Handle chat messages
    socket.on('chatMessage', (data) => {
        const messageData = {
            id: socket.id,
            username: data.username,
            message: data.message,
            timestamp: new Date()
        };
        
        // Broadcast message to all connected clients
        io.emit('message', messageData);
        
        console.log(`Message from ${data.username}: ${data.message}`);
    });

    // Handle typing indicator
    socket.on('typing', (data) => {
        socket.broadcast.emit('typing', {
            username: data.username,
            isTyping: data.isTyping
        });
    });

    // Handle user disconnection
    socket.on('disconnect', () => {
        if (socket.username) {
            // Remove user from users array
            users = users.filter(user => user.id !== socket.id);
            
            // Notify all users about user leaving
            socket.broadcast.emit('userLeft', {
                username: socket.username,
                message: `${socket.username} left the chat`,
                timestamp: new Date()
            });
            
            // Update users list for all clients
            io.emit('updateUsersList', users);
            
            console.log(`${socket.username} disconnected`);
        }
    });
});

// Start server
server.listen(PORT, () => {
    console.log(`Chat server running on http://localhost:${PORT}`);
});''',

    'public/index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Real-Time Chat App</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <!-- Join Screen -->
        <div id="joinScreen" class="join-screen">
            <div class="join-card">
                <h1><i class="fas fa-comments"></i> Real-Time Chat</h1>
                <p>Enter your name to join the conversation</p>
                <form id="joinForm">
                    <input type="text" id="usernameInput" placeholder="Your Name" required maxlength="20">
                    <button type="submit">
                        <i class="fas fa-sign-in-alt"></i> Join Chat
                    </button>
                </form>
            </div>
        </div>

        <!-- Chat Screen -->
        <div id="chatScreen" class="chat-screen" style="display: none;">
            <div class="chat-container">
                <!-- Header -->
                <div class="chat-header">
                    <h2><i class="fas fa-comments"></i> Chat Room</h2>
                    <div class="user-info">
                        <span id="currentUser"></span>
                        <button id="leaveBtn" class="leave-btn">
                            <i class="fas fa-sign-out-alt"></i> Leave
                        </button>
                    </div>
                </div>

                <!-- Main Chat Area -->
                <div class="chat-main">
                    <!-- Messages Area -->
                    <div class="messages-area">
                        <div id="messages" class="messages"></div>
                        <div id="typingIndicator" class="typing-indicator"></div>
                    </div>

                    <!-- Users List -->
                    <div class="users-area">
                        <h3><i class="fas fa-users"></i> Online Users</h3>
                        <div id="usersList" class="users-list"></div>
                    </div>
                </div>

                <!-- Message Input -->
                <div class="message-input-area">
                    <form id="messageForm">
                        <input type="text" id="messageInput" placeholder="Type your message..." 
                               autocomplete="off" maxlength="500">
                        <button type="submit">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <script src="/socket.io/socket.io.js"></script>
    <script src="script.js"></script>
</body>
</html>''',

    'public/style.css': '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    height: 100vh;
    overflow: hidden;
}

.container {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Join Screen Styles */
.join-screen {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    width: 100vw;
}

.join-card {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    text-align: center;
    min-width: 300px;
    animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.join-card h1 {
    color: #667eea;
    margin-bottom: 0.5rem;
    font-size: 1.8rem;
}

.join-card p {
    color: #666;
    margin-bottom: 1.5rem;
}

.join-card input {
    width: 100%;
    padding: 12px;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
    margin-bottom: 1rem;
    transition: border-color 0.3s;
}

.join-card input:focus {
    outline: none;
    border-color: #667eea;
}

.join-card button {
    width: 100%;
    padding: 12px;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.3s;
}

.join-card button:hover {
    background: #5a6fd8;
}

/* Chat Screen Styles */
.chat-screen {
    width: 100vw;
    height: 100vh;
}

.chat-container {
    width: 100%;
    height: 100%;
    background: white;
    display: flex;
    flex-direction: column;
}

.chat-header {
    background: #667eea;
    color: white;
    padding: 1rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.chat-header h2 {
    font-size: 1.3rem;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.leave-btn {
    background: rgba(255,255,255,0.2);
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s;
}

.leave-btn:hover {
    background: rgba(255,255,255,0.3);
}

.chat-main {
    flex: 1;
    display: flex;
    overflow: hidden;
}

.messages-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: #f8f9fa;
}

.messages {
    flex: 1;
    padding: 1rem;
    overflow-y: auto;
    max-height: calc(100vh - 140px);
}

.message {
    margin-bottom: 1rem;
    animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.message.own {
    text-align: right;
}

.message .message-content {
    display: inline-block;
    max-width: 70%;
    padding: 10px 15px;
    border-radius: 18px;
    word-wrap: break-word;
}

.message.own .message-content {
    background: #667eea;
    color: white;
}

.message.other .message-content {
    background: white;
    border: 1px solid #ddd;
    color: #333;
}

.message .message-info {
    font-size: 0.8rem;
    color: #666;
    margin-top: 3px;
}

.system-message {
    text-align: center;
    color: #666;
    font-style: italic;
    font-size: 0.9rem;
    margin: 10px 0;
    padding: 5px;
    background: rgba(102, 126, 234, 0.1);
    border-radius: 10px;
}

.typing-indicator {
    padding: 0 1rem;
    color: #666;
    font-style: italic;
    font-size: 0.9rem;
    min-height: 20px;
}

.users-area {
    width: 250px;
    background: white;
    border-left: 1px solid #ddd;
    padding: 1rem;
}

.users-area h3 {
    color: #667eea;
    margin-bottom: 1rem;
    font-size: 1rem;
}

.users-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.user-item {
    padding: 8px 12px;
    background: #f8f9fa;
    border-radius: 8px;
    border-left: 3px solid #667eea;
    font-size: 0.9rem;
}

.message-input-area {
    padding: 1rem 1.5rem;
    background: white;
    border-top: 1px solid #ddd;
}

.message-input-area form {
    display: flex;
    gap: 10px;
}

.message-input-area input {
    flex: 1;
    padding: 12px 15px;
    border: 2px solid #ddd;
    border-radius: 25px;
    font-size: 1rem;
    transition: border-color 0.3s;
}

.message-input-area input:focus {
    outline: none;
    border-color: #667eea;
}

.message-input-area button {
    padding: 12px 20px;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 25px;
    cursor: pointer;
    transition: background 0.3s;
}

.message-input-area button:hover {
    background: #5a6fd8;
}

/* Responsive Design */
@media (max-width: 768px) {
    .chat-main {
        flex-direction: column;
    }
    
    .users-area {
        width: 100%;
        max-height: 150px;
        overflow-y: auto;
    }
    
    .users-list {
        flex-direction: row;
        flex-wrap: wrap;
    }
    
    .message .message-content {
        max-width: 85%;
    }
}''',

    'public/script.js': '''// Initialize Socket.io
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
});''',

    'README.md': '''# Real-Time Chat Application

A simple real-time chat application built with Node.js, Express.js, and Socket.io.

## Features

- **Real-time messaging** between multiple users
- **User join/leave notifications**
- **Online users list**
- **Typing indicators**
- **Responsive design** for mobile and desktop
- **Clean and modern UI**

## Technologies Used

- **Backend:** Node.js, Express.js, Socket.io
- **Frontend:** HTML5, CSS3, JavaScript (ES6)
- **Real-time Communication:** WebSockets via Socket.io

## Installation & Setup

### Prerequisites
- Node.js (v14 or higher)
- npm (comes with Node.js)

### Steps

1. **Clone or download the project**
   ```bash
   # If using git
   git clone <repository-url>
   cd realtime-chat-app
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the server**
   ```bash
   # For development (with auto-restart)
   npm run dev
   
   # For production
   npm start
   ```

4. **Open in browser**
   - Navigate to `http://localhost:3000`
   - Open multiple tabs to test real-time messaging

## Project Structure

```
realtime-chat-app/
├── server.js           # Main server file
├── package.json        # Project dependencies
├── README.md          # Project documentation
└── public/            # Static files
    ├── index.html     # Main HTML file
    ├── style.css      # Styles
    └── script.js      # Client-side JavaScript
```

## Usage

1. **Join the chat:**
   - Enter your name on the welcome screen
   - Click "Join Chat"

2. **Send messages:**
   - Type your message in the input field
   - Press Enter or click the send button

3. **View online users:**
   - See all currently connected users in the sidebar
   - Users are updated in real-time

4. **Leave the chat:**
   - Click the "Leave" button in the header
   - Or simply close the browser tab

## Features Explained

### Real-time Messaging
- Messages are instantly delivered to all connected users
- Uses WebSocket connection for low-latency communication

### User Management
- Tracks all connected users
- Displays join/leave notifications
- Updates online users list in real-time

### Typing Indicators
- Shows when other users are typing
- Automatically clears after 1 second of inactivity

### Responsive Design
- Works on desktop, tablet, and mobile devices
- Adaptive layout for different screen sizes

## Future Enhancements

- [ ] Message persistence (database integration)
- [ ] Private messaging
- [ ] Chat rooms/channels
- [ ] File sharing
- [ ] User authentication
- [ ] Message reactions/emojis
- [ ] Message search functionality

## Learning Outcomes

This project demonstrates:
- **Full-stack JavaScript development**
- **Real-time web application development**
- **WebSocket communication**
- **Event-driven programming**
- **Client-server architecture**
- **Responsive web design**

## Author

**Aman Agrawal**
- Email: agrawal280503@gmail.com
- LinkedIn: https://www.linkedin.com/in/aman-agrawal-460040310/

## License

MIT License - Feel free to use this project for learning and development purposes.
'''
}

# Write all files
for filename, content in project_files.items():
    print(f"Creating: {filename}")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("\n✅ All project files created successfully!")
print("\nProject Structure:")
print("📁 realtime-chat-app/")
print("├── 📄 package.json")
print("├── 📄 server.js")
print("├── 📄 README.md")
print("└── 📁 public/")
print("    ├── 📄 index.html")
print("    ├── 📄 style.css")
print("    └── 📄 script.js")