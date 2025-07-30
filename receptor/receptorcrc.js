// receptor.js

const prompt = require("prompt-sync")({ sigint: true });
const { iniciarServidor }    = require("./transmision");
const { verificarIntegridad } = require("./enlacecrc");
const { decodificarMensaje }  = require("./presentation");
const { mostrarMensaje, mostrarError } = require("./applicationcrc");

// Recibe el puerto como argumento
const port = parseInt(process.argv[2], 10);
if (isNaN(port)) {
  console.error("Uso: node receptor.js <PUERTO>");
  process.exit(1);
}

iniciarServidor(port, trama => {
  console.log("\n---- TRAMA RECIBIDA ----");
  console.log(trama);

  if (!verificarIntegridad(trama)) {
    mostrarError();
    return;
  }

  // Extrae datos (quita últimos 32 bits de CRC)
  const dataBits = trama.slice(0, -32);
  const texto    = decodificarMensaje(dataBits);
  mostrarMensaje(texto);
});
