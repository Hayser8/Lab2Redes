// enlace.js

// CRC‑32 básico con tabla
const CRC32 = (() => {
  const table = new Uint32Array(256);
  for (let i = 0; i < 256; i++) {
    let c = i;
    for (let j = 0; j < 8; j++) {
      c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    }
    table[i] = c >>> 0;
  }
  return {
    compute(buf) {
      let crc = 0 ^ (-1);
      for (const b of buf) {
        crc = (crc >>> 8) ^ table[(crc ^ b) & 0xFF];
      }
      return (crc ^ (-1)) >>> 0;
    }
  };
})();

function calcularIntegridad(dataBits) {
  // dataBits: cadena de '0'/'1', longitud múltiplo de 8
  const nBytes = dataBits.length / 8;
  const buf = Buffer.alloc(nBytes);
  for (let i = 0; i < nBytes; i++) {
    buf[i] = parseInt(dataBits.slice(i*8, i*8+8), 2);
  }
  const crc = CRC32.compute(buf);
  const crcBits = crc.toString(2).padStart(32, '0');
  return dataBits + crcBits;
}

function verificarIntegridad(trama) {
  const dataBits = trama.slice(0, -32);
  const crcBits  = trama.slice(-32);
  const nBytes = dataBits.length / 8;
  const buf = Buffer.alloc(nBytes);
  for (let i = 0; i < nBytes; i++) {
    buf[i] = parseInt(dataBits.slice(i*8, i*8+8), 2);
  }
  const calcCrc = CRC32.compute(buf).toString(2).padStart(32, '0');
  return calcCrc === crcBits;
}

module.exports = { calcularIntegridad, verificarIntegridad };
