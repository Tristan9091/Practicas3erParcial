const API_BASE = "http://127.0.0.1:8000";

async function request(metodo, ruta, { body = null, auth = false } = {}) {
  const headers = {};
  if (body) headers["Content-Type"] = "application/json";
  if (auth) {
    const token = obtenerToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }
  const respuesta = await fetch(`${API_BASE}${ruta}`, {
    method: metodo,
    headers,
    body: body ? JSON.stringify(body) : null,
  });
  if (!respuesta.ok) {
    let detalle = "Error en la petición";
    try {
      const data = await respuesta.json();
      if (Array.isArray(data.detail)) {
        detalle = data.detail.map((e) => e.msg).join(", ");
      } else if (data.detail) {
        detalle = data.detail;
      }
    } catch (e) {}
    throw new Error(detalle);
  }
  if (respuesta.status === 204) return null;
  return respuesta.json();
}

function urlImagen(ruta) {
  if (!ruta) return "https://placehold.co/400x300?text=Sin+imagen";
  if (ruta.startsWith("http")) return ruta;
  return `${API_BASE}${ruta}`;
}

async function login(email, password) {
  const datos = new URLSearchParams();
  datos.append("username", email);
  datos.append("password", password);
  const respuesta = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    body: datos,
  });
  if (!respuesta.ok) {
    const err = await respuesta.json().catch(() => ({}));
    throw new Error(err.detail || "Credenciales inválidas");
  }
  return respuesta.json();
}

function registrar(nombre, email, password) {
  return request("POST", "/auth/register", {
    body: { nombre, email, password },
  });
}

function iniciarConversacion(clienteId) {
  return request("POST", "/chat/conversaciones", {
    body: { cliente_id: clienteId },
  });
}

function listarUsuarios() {
  return request("GET", "/auth/usuarios", { auth: true });
}

function cambiarRolUsuario(email, rol) {
  return request("PATCH", `/auth/usuarios/${encodeURIComponent(email)}/rol`, {
    body: { rol },
    auth: true,
  });
}

function listarProductos() {
  return request("GET", "/productos");
}

function crearProducto(producto) {
  return request("POST", "/productos", { body: producto, auth: true });
}

function actualizarProducto(id, producto) {
  return request("PUT", `/productos/${id}`, { body: producto, auth: true });
}

function eliminarProducto(id) {
  return request("DELETE", `/productos/${id}`, { auth: true });
}

async function subirImagen(archivo) {
  const datos = new FormData();
  datos.append("archivo", archivo);
  const respuesta = await fetch(`${API_BASE}/productos/upload-imagen`, {
    method: "POST",
    headers: { Authorization: `Bearer ${obtenerToken()}` },
    body: datos,
  });
  if (!respuesta.ok) {
    const err = await respuesta.json().catch(() => ({}));
    throw new Error(err.detail || "Error al subir la imagen");
  }
  return respuesta.json();
}

function crearPerfil(perfil) {
  return request("POST", "/perfiles", { body: perfil, auth: true });
}

function crearOrden(orden) {
  return request("POST", "/ordenes", { body: orden, auth: true });
}

function listarOrdenesPorPerfil(perfilId) {
  return request("GET", `/ordenes/perfil/${perfilId}`, { auth: true });
}

function cancelarOrden(id) {
  return request("PATCH", `/ordenes/${id}/cancelar`, { auth: true });
}

function listarTodasLasOrdenes() {
  return request("GET", "/ordenes", { auth: true });
}

function actualizarEstadoOrden(id, estado) {
  return request("PATCH", `/ordenes/${id}/estado`, {
    body: { estado },
    auth: true,
  });
}
