addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  // Python script you want to serve as a downloadable file, encoded in Base64
  const pythonScriptBase64 = `
  your base64 utf-8 encoded python script here
  `;

  // Decode the Base64-encoded script and create a downloadable response
  const decodedScript = atob(pythonScriptBase64);
  const blob = new Blob([decodedScript], { type: 'application/octet-stream' });
  const response = new Response(blob, {
    headers: {
      'Content-Type': 'application/octet-stream',
      'Content-Disposition': 'attachment; filename="file-name.py"',
    },
  });

  return response;
}
