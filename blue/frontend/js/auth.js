function guardarSesion(data) {
  localStorage.setItem("access_token", data.access_token);
  if (data.refresh_token) {
    localStorage.setItem("refresh_token", data.refresh_token);
  }
}

function obtenerToken() {
  return localStorage.getItem("access_token");
}

function decodificarToken() {
  const token = obtenerToken();
  if (!token) return null;
  try {
    const payload = token.split(".")[1];
    const json = atob(payload.replace(/-/g, "+").replace(/_/g, "/"));
    return JSON.parse(json);
  } catch (e) {
    return null;
  }
}

function obtenerRol() {
  const datos = decodificarToken();
  return datos ? datos.rol : null;
}

// El email viene en "sub" (subject), que es el estándar del JWT
function obtenerEmail() {
  const datos = decodificarToken();
  return datos ? datos.sub : null;
}

// ¿Hay sesión activa? (true si existe un token)
function estaAutenticado() {
  return !!obtenerToken();
}

// Cierra sesión: borra todo y manda al login
function cerrarSesion() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  window.location.href = "login.html";
}

// Protege una página: si no hay sesión, o el rol no está permitido, redirige.
// Ejemplo de uso en admin.js -> protegerPagina(["admin", "operador"])
function protegerPagina(rolesPermitidos = null) {
  if (!estaAutenticado()) {
    window.location.href = "login.html";
    return;
  }
  if (rolesPermitidos && !rolesPermitidos.includes(obtenerRol())) {
    alert("No tienes permisos para entrar a esta página");
    window.location.href = "index.html";
  }
}
