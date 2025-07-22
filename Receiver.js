const readline = require('readline');

function hammingDecode(code) {
  const n = code.length;
  // Calcular cuántos bits de paridad hay (mayor r tal que 2^r < n+1)
  let r = 0;
  while ((1 << r) < n + 1) r++;
  let errorPos = 0;
  // Verificar cada bit de paridad
  for (let i = 0; i < r; i++) {
    const parityPos = 1 << i;
    let parity = 0;
    for (let k = 1; k <= n; k++) {
      if ((k & parityPos) !== 0) {
        parity ^= parseInt(code[k - 1], 10);
      }
    }
    if (parity !== 0) errorPos += parityPos;
  }
  let corrected = code.split('');
  if (errorPos > 0 && errorPos <= n) {
    console.log(`Error detectado en posición ${errorPos}. Corrigiendo...`);
    corrected[errorPos - 1] = corrected[errorPos - 1] === '0' ? '1' : '0';
  } else if (errorPos === 0) {
    console.log('No se detectaron errores.');
  } else {
    console.log('Error en posición fuera de rango, no se corrige.');
  }
  const correctedCode = corrected.join('');
  // Extraer bits de datos
  let dataBits = '';
  for (let i = 1; i <= n; i++) {
    if ((i & (i - 1)) !== 0) dataBits += corrected[i - 1];
  }
  console.log('Trama recibida (corregida si aplica):', correctedCode);
  console.log('Datos extraídos:', dataBits);
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});
rl.question('Ingrese la trama codificada (Hamming): ', (code) => {
  hammingDecode(code.trim());
  rl.close();
});
