const io = require('socket.io-client');
const socket = io('http://localhost:5000');

socket.on('connect', () => {
  console.log('Connected to server');

  // Emit a 'transaction' event
  socket.emit('transaction', {
    pdf_data: 'Alice',
    pdf_name: 'Alice.pdf'
  });
});

socket.on('transaction', (transaction) => {
  console.log('Received transaction:', transaction);
});

socket.on('disconnect', () => {
  console.log('Disconnected from server');
});