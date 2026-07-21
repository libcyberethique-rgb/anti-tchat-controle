const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);
const path = require('path');

// Sert la page HTML
app.use(express.static(path.join(__dirname, 'public')));

io.on('connection', (socket) => {
  let userPseudo = '';

  // Quand un pote rejoint avec son pseudo
  socket.on('join', (pseudo) => {
    userPseudo = pseudo;
    io.emit('message', {
      type: 'system',
      text: `*** ${pseudo} a rejoint le tchat ! ***`
    });
  });

  // Quand un message est envoyé
  socket.on('chatMessage', (msg) => {
    // Renvoie le message à TOUT LE MONDE
    socket.broadcast.emit('message', {
      type: 'received',
      pseudo: userPseudo,
      text: msg
    });
  });

  // Déconnexion
  socket.on('disconnect', () => {
    if (userPseudo) {
      io.emit('message', {
        type: 'system',
        text: `*** ${userPseudo} a quitté le tchat. ***`
      });
    }
  });
});

const PORT = process.env.PORT || 3000;
http.listen(PORT, () => {
  console.log(`Serveur démarré sur le port ${PORT}`);
});
