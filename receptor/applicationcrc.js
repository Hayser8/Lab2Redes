// application.js

function mostrarMensaje(texto) {
  console.log("\n---- MENSAJE DECODIFICADO ----");
  console.log(texto);
}

function mostrarError() {
  console.error("\n¡¡Error de integridad!! El mensaje está corrupto.");
}

module.exports = { mostrarMensaje, mostrarError };
