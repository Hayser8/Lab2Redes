#!/usr/bin/env node
const POLY = BigInt(0x104C11DB7);

function verifyCRC32(bitstr) {
  const n = bitstr.length;
  if (n <= 32) return false;  // necesita al menos 1 bit + 32 de CRC

  // Convierte toda la cadena a BigInt
  let rem = BigInt('0b' + bitstr);
  // División polinómica
  for (let bit = BigInt(n - 1); bit >= BigInt(32); bit--) {
    if ((rem >> bit) & BigInt(1)) {
      rem ^= POLY << (bit - BigInt(32));
    }
  }
  // Si el resto final es 0, CRC válido
  return (rem & BigInt(0xFFFFFFFF)) === BigInt(0);
}

function extractData(bitstr) {
  return bitstr.slice(0, -32);
}

const [,, input] = process.argv;
if (!input) {
  console.log('Uso: node crc32_receiver.js <trama_codificada_bits>');
  process.exit(1);
}

const valid = verifyCRC32(input.trim());
if (valid) {
  console.log('CRC VÁLIDO ✅');
  console.log('Datos originales:', extractData(input.trim()));
} else {
  console.log('ERROR DE CRC ❌ — trama corrupta o mal ingresada.');
}
