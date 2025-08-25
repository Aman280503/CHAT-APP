# Real-Time Chat Application

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
