const express = require('express');
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
});