const prompt = require("prompt-sync")({ sigint:true });
const { iniciarServidor } = require("./transmision");
const { hammingDecodeMessage } = require("./enlace");
const { decodificarMensaje } = require("./presentation");
const { mostrarMensaje } = require("./application");

const port = parseInt(prompt("Puerto en el que escuchar (p.ej. 5001): "));
iniciarServidor(port, code => {
  console.log("\n---- TRAMA RECIBIDA ----");
  console.log(code);

  // ENLACE
  const dataBits = hammingDecodeMessage(code);

  // PRESENTACIÓN
  const texto = decodificarMensaje(dataBits);

  // APLICACIÓN
  mostrarMensaje(texto);
});