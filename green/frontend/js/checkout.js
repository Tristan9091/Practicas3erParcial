protegerPagina();
document.getElementById("usuario-email").textContent = obtenerEmail();
document.getElementById("btn-salir").addEventListener("click", cerrarSesion);

function obtenerCarrito() {
  return JSON.parse(localStorage.getItem("carrito") || "[]");
}

function renderResumen() {
  const carrito = obtenerCarrito();
  const cont = document.getElementById("resumen-items");
  const totalEl = document.getElementById("resumen-total");

  if (carrito.length === 0) {
    cont.innerHTML = `<p class="text-muted">Tu carrito está vacío. <a href="index.html">Ver catálogo</a></p>`;
    document.getElementById("btn-pagar").disabled = true;
  } else {
    cont.innerHTML = carrito
      .map(
        (item) => `
      <div class="d-flex justify-content-between mb-2">
        <span>${item.nombre} <span class="text-muted">× ${item.cantidad}</span></span>
        <span>$${(item.precio * item.cantidad).toFixed(2)}</span>
      </div>`,
      )
      .join("");
  }

  const total = carrito.reduce((s, i) => s + i.precio * i.cantidad, 0);
  totalEl.textContent = `$${total.toFixed(2)}`;
}

function llavePerfil() {
  return `perfil_${obtenerEmail()}`;
}

function obtenerPerfilId() {
  return localStorage.getItem(llavePerfil());
}

async function asegurarPerfil(nombre, direccion, metodoPago) {
  let perfilId = obtenerPerfilId();
  if (perfilId) return perfilId;

  const perfil = await crearPerfil({
    nombre: nombre,
    email: obtenerEmail(),
    direccion: direccion,
    metodo_pago: metodoPago,
    preferencias: [],
  });
  localStorage.setItem(llavePerfil(), perfil.id);
  return perfil.id;
}

function mostrarMensaje(texto, tipo = "danger") {
  const caja = document.getElementById("checkout-mensaje");
  caja.textContent = texto;
  caja.className = `alert alert-${tipo}`;
}

document.getElementById("btn-pagar").addEventListener("click", async () => {
  const carrito = obtenerCarrito();
  const nombre = document.getElementById("form-nombre").value.trim();
  const direccion = document.getElementById("form-direccion").value.trim();
  const metodoPago = document.getElementById("form-pago").value;

  if (carrito.length === 0) {
    mostrarMensaje("Tu carrito está vacío");
    return;
  }
  if (!nombre || !direccion) {
    mostrarMensaje("Completa nombre y dirección");
    return;
  }

  const boton = document.getElementById("btn-pagar");
  boton.disabled = true;
  boton.textContent = "Procesando...";

  try {
    const perfilId = await asegurarPerfil(nombre, direccion, metodoPago);

    const items = carrito.map((item) => ({
      producto_id: item.id,
      nombre_producto: item.nombre,
      precio_unitario: item.precio,
      cantidad: item.cantidad,
    }));

    await crearOrden({
      perfil_id: perfilId,
      items: items,
      direccion_envio: direccion,
      metodo_pago: metodoPago,
    });

    localStorage.removeItem("carrito");
    renderResumen();
    mostrarMensaje("¡Compra realizada con éxito! 🎉", "success");
    cargarHistorial();
  } catch (e) {
    mostrarMensaje("No se pudo completar la compra: " + e.message);
  } finally {
    boton.disabled = false;
    boton.textContent = "Confirmar compra";
  }
});

async function cargarHistorial() {
  const cont = document.getElementById("historial");
  const perfilId = obtenerPerfilId();

  if (!perfilId) {
    cont.innerHTML = `<p class="text-muted">Aún no tienes pedidos.</p>`;
    return;
  }

  try {
    const ordenes = await listarOrdenesPorPerfil(perfilId);
    if (!ordenes || ordenes.length === 0) {
      cont.innerHTML = `<p class="text-muted">Aún no tienes pedidos.</p>`;
      return;
    }

    cont.innerHTML = ordenes
      .map(
        (o) => `
      <div class="card mb-2">
        <div class="card-body py-2">
          <div class="d-flex justify-content-between align-items-center">
            <small class="text-muted">${new Date(o.fecha).toLocaleDateString()}</small>
            <span class="badge ${colorEstado(o.estado)}">${o.estado}</span>
          </div>
          <div class="my-1 small">
            ${o.items.map((i) => `${i.nombre_producto} ×${i.cantidad}`).join(", ")}
          </div>
          <div class="d-flex justify-content-between align-items-center">
            <strong>$${o.total.toFixed(2)}</strong>
            ${
              o.estado === "pendiente"
                ? `<button class="btn btn-sm btn-outline-danger" onclick="anularOrden('${o.id}')">Cancelar</button>`
                : ""
            }
          </div>
        </div>
      </div>`,
      )
      .join("");
  } catch (e) {
    cont.innerHTML = `<p class="text-danger">Error al cargar pedidos: ${e.message}</p>`;
  }
}

function colorEstado(estado) {
  const colores = {
    pendiente: "bg-warning text-dark",
    pagada: "bg-info text-dark",
    enviada: "bg-primary",
    entregada: "bg-success",
    cancelada: "bg-secondary",
  };
  return colores[estado] || "bg-secondary";
}

async function anularOrden(id) {
  if (!confirm("¿Seguro que quieres cancelar este pedido?")) return;
  try {
    await cancelarOrden(id);
    cargarHistorial();
  } catch (e) {
    alert("No se pudo cancelar: " + e.message);
  }
}

renderResumen();
cargarHistorial();
