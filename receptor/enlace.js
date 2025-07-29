function hammingDecodeBlock(codeBits) {
  const n = 12;
  const r = 4;
  // 1) detecta error
  let errorPos = 0;
  for (let i = 0; i < r; i++) {
    const p = 1 << i;
    let sum = 0;
    for (let j = p-1; j < n; j += 2*p) {
      for (let k = j; k < j+p && k < n; k++) {
        if (codeBits[k] === '1') sum++;
      }
    }
    if (sum % 2 !== 0) errorPos += p;
  }
  // 2) corrige si hace falta
  let bitsArr = codeBits.split("");
  if (errorPos !== 0) {
    const idx = errorPos - 1;
    bitsArr[idx] = bitsArr[idx] === '0' ? '1' : '0';
    console.warn("⚠️  Se corrigió un bit con Hamming en bloque.");
  }
  // 3) extrae datos (quita 1,2,4,8)
  const data = bitsArr
    .filter((_, i) => ((i+1)&i)!==0)
    .join("");
  return data;
}

function hammingDecodeMessage(code) {
  const bloques = [];
  for (let i = 0; i < code.length; i += 12) {
    bloques.push(code.slice(i, i+12));
  }
  return bloques.map(hammingDecodeBlock).join("");
}

module.exports = { hammingDecodeMessage };