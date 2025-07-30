// receptor.js

const { iniciarServidor } = require("./transmision");
const { hammingDecodeMessage } = require("./enlace");
const { decodificarMensaje } = require("./presentation");
const { mostrarMensaje } = require("./application");

// ********************
//  Ahora recibimos el puerto por argv
const port = parseInt(process.argv[2], 10);
if (isNaN(port)) {
  console.error("Uso: node receptor.js <PUERTO>");
  process.exit(1);
}
console.log(`Receptor escuchando en puerto ${port}`);
// ********************

iniciarServidor(port, code => {
  console.log("\n---- TRAMA RECIBIDA ----");
  console.log(code);

  // ENLACE: decode + corregir
  const dataBits = hammingDecodeMessage(code);

  // PRESENTACIÓN: bits → texto
  const texto = decodificarMensaje(dataBits);

  // APLICACIÓN: mostrar
  mostrarMensaje(texto);
});
