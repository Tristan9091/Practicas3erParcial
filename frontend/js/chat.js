(function () {
  const cajaMensajes = document.getElementById("chat-mensajes");
  if (!cajaMensajes) return;

  const input = document.getElementById("chat-input");
  const boton = document.getElementById("chat-enviar");
  const clienteId = obtenerEmail() || "invitado";

  let socket;

  async function conectar() {
    try {
      const conv = await iniciarConversacion(clienteId);
      const WS_BASE = API_BASE.replace(/^http/, "ws");

      socket = new WebSocket(`${WS_BASE}/ws/chat/${conv.conversacion_id}`);

      socket.onmessage = (evento) => {
        const msg = JSON.parse(evento.data);
        agregarMensaje(msg.autor, msg.contenido);
      };
      socket.onclose = () => agregarMensaje("sistema", "Conexión cerrada.");
    } catch (e) {
      agregarMensaje("sistema", "No se pudo conectar al chat: " + e.message);
    }
  }

  function agregarMensaje(autor, contenido) {
    const esCliente = autor === "cliente";
    const fila = document.createElement("div");
    fila.className = `d-flex mb-2 ${esCliente ? "justify-content-end" : "justify-content-start"}`;

    let etiqueta = "Asistente";
    if (autor === "cliente") etiqueta = "Tú";
    else if (autor === "sistema") etiqueta = "Sistema";
    else if (autor === "agente") etiqueta = "Agente";

    const color = esCliente
      ? "bg-brand text-white"
      : autor === "sistema"
        ? "bg-light text-muted border"
        : autor === "agente"
          ? "bg-warning-subtle border"
          : "bg-white border";

    fila.innerHTML = `
      <div class="chat-burbuja ${color}">
        <div class="chat-autor small fw-bold">${etiqueta}</div>
        <div>${contenido}</div>
      </div>`;
    cajaMensajes.appendChild(fila);
    cajaMensajes.scrollTop = cajaMensajes.scrollHeight;
  }

  function enviar() {
    const texto = input.value.trim();
    if (!texto) return;
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      agregarMensaje("sistema", "No hay conexión con el chat.");
      return;
    }
    socket.send(texto);
    input.value = "";
  }

  boton.addEventListener("click", enviar);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") enviar();
  });

  conectar();
})();
