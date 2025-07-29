const net = require("net");

function iniciarServidor(port, onData) {
  net.createServer(socket => {
    socket.on("data", data => onData(data.toString().trim()));
  }).listen(port, () => {
    console.log(`🚀 Receptor escuchando en puerto ${port}`);
  });
}

module.exports = { iniciarServidor };