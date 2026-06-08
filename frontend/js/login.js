if (estaAutenticado()) {
  redirigirPorRol();
}

function redirigirPorRol() {
  if (obtenerRol() === "admin") {
    window.location.href = "admin.html";
  } else {
    window.location.href = "index.html";
  }
}

function mostrarMensaje(texto, tipo = "danger") {
  const caja = document.getElementById("mensaje");
  caja.textContent = texto;
  caja.className = `alert alert-${tipo}`;
}

document.getElementById("btn-login").addEventListener("click", async () => {
  const email = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value;

  if (!email || !password) {
    mostrarMensaje("Completa correo y contraseña");
    return;
  }

  try {
    const data = await login(email, password);
    guardarSesion(data);
    redirigirPorRol();
  } catch (e) {
    mostrarMensaje(e.message);
  }
});

document.getElementById("btn-registro").addEventListener("click", async () => {
  const nombre = document.getElementById("reg-nombre").value.trim();
  const email = document.getElementById("reg-email").value.trim();
  const password = document.getElementById("reg-password").value;

  if (!nombre || !email || !password) {
    mostrarMensaje("Completa todos los campos");
    return;
  }
  if (password.length < 6) {
    mostrarMensaje("La contraseña debe tener al menos 6 caracteres");
    return;
  }

  try {
    await registrar(nombre, email, password);
    const data = await login(email, password);
    guardarSesion(data);
    redirigirPorRol();
  } catch (e) {
    mostrarMensaje(e.message);
  }
});
