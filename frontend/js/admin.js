protegerPagina(["admin", "operador"]);
document.getElementById("usuario-email").textContent = obtenerEmail();
document.getElementById("btn-salir").addEventListener("click", cerrarSesion);
const esAdmin = obtenerRol() === "admin";

if (!esAdmin) {
  document.getElementById("btn-nuevo-producto").classList.add("d-none");
  const navUsuarios = document.querySelector(
    '[data-bs-target="#tab-usuarios"]',
  );
  if (navUsuarios) navUsuarios.closest("li").classList.add("d-none");
}

const modalProducto = new bootstrap.Modal(
  document.getElementById("modal-producto"),
);

let productosAdmin = [];
let editandoId = null;
let imagenesActuales = [];

async function cargarProductos() {
  productosAdmin = await listarProductos();
  const tbody = document.getElementById("tabla-productos");
  tbody.innerHTML = productosAdmin
    .map(
      (p) => `
    <tr>
      <td><img src="${urlImagen(p.imagenes && p.imagenes[0])}" class="admin-thumb"></td>
      <td>${p.nombre}</td>
      <td>$${p.precio.toFixed(2)}</td>
      <td>${p.stock}</td>
      <td>${p.vendedor || "-"}</td>
      <td class="text-end">
        <button class="btn btn-sm btn-outline-primary" onclick="editarProducto('${p.id}')">Editar</button>
        ${esAdmin ? `<button class="btn btn-sm btn-outline-danger" onclick="borrarProducto('${p.id}')">Eliminar</button>` : ""}
      </td>
    </tr>`,
    )
    .join("");
}

document.getElementById("btn-nuevo-producto").addEventListener("click", () => {
  editandoId = null;
  imagenesActuales = [];
  document.getElementById("modal-titulo").textContent = "Nuevo producto";
  limpiarFormularioProducto();
  modalProducto.show();
});

function editarProducto(id) {
  const p = productosAdmin.find((x) => x.id === id);
  if (!p) return;
  editandoId = id;
  imagenesActuales = p.imagenes || [];
  document.getElementById("modal-titulo").textContent = "Editar producto";
  document.getElementById("prod-nombre").value = p.nombre;
  document.getElementById("prod-descripcion").value = p.descripcion || "";
  document.getElementById("prod-precio").value = p.precio;
  document.getElementById("prod-stock").value = p.stock;
  document.getElementById("prod-vendedor").value = p.vendedor || "";
  const preview = document.getElementById("prod-preview");
  if (imagenesActuales[0]) {
    preview.src = urlImagen(imagenesActuales[0]);
    preview.classList.remove("d-none");
  } else {
    preview.classList.add("d-none");
  }
  document.getElementById("prod-imagen").value = "";
  document.getElementById("modal-mensaje").classList.add("d-none");
  modalProducto.show();
}

function limpiarFormularioProducto() {
  [
    "prod-nombre",
    "prod-descripcion",
    "prod-precio",
    "prod-stock",
    "prod-vendedor",
    "prod-imagen",
  ].forEach((id) => (document.getElementById(id).value = ""));
  document.getElementById("prod-preview").classList.add("d-none");
  document.getElementById("modal-mensaje").classList.add("d-none");
}

document.getElementById("prod-imagen").addEventListener("change", (e) => {
  const archivo = e.target.files[0];
  const preview = document.getElementById("prod-preview");
  if (archivo) {
    preview.src = URL.createObjectURL(archivo);
    preview.classList.remove("d-none");
  }
});

document
  .getElementById("btn-guardar-producto")
  .addEventListener("click", async () => {
    const nombre = document.getElementById("prod-nombre").value.trim();
    const descripcion = document
      .getElementById("prod-descripcion")
      .value.trim();
    const precio = parseFloat(document.getElementById("prod-precio").value);
    const stock = parseInt(document.getElementById("prod-stock").value) || 0;
    const vendedor = document.getElementById("prod-vendedor").value.trim();
    const archivo = document.getElementById("prod-imagen").files[0];

    if (!nombre) {
      mostrarMensajeModal("El nombre es obligatorio");
      return;
    }
    if (!precio || precio <= 0) {
      mostrarMensajeModal("El precio debe ser mayor a 0");
      return;
    }

    const boton = document.getElementById("btn-guardar-producto");
    boton.disabled = true;
    boton.textContent = "Guardando...";

    try {
      let imagenes = imagenesActuales;
      if (archivo) {
        const subida = await subirImagen(archivo);
        imagenes = [subida.url];
      }

      const datos = { nombre, descripcion, vendedor, precio, stock, imagenes };

      if (editandoId) {
        await actualizarProducto(editandoId, datos);
      } else {
        await crearProducto(datos);
      }

      modalProducto.hide();
      cargarProductos();
    } catch (e) {
      mostrarMensajeModal("Error al guardar: " + e.message);
    } finally {
      boton.disabled = false;
      boton.textContent = "Guardar";
    }
  });

async function borrarProducto(id) {
  if (!confirm("¿Eliminar este producto?")) return;
  try {
    await eliminarProducto(id);
    cargarProductos();
  } catch (e) {
    alert("No se pudo eliminar: " + e.message);
  }
}

function mostrarMensajeModal(texto) {
  const caja = document.getElementById("modal-mensaje");
  caja.textContent = texto;
  caja.className = "alert alert-danger";
}

const ESTADOS = ["pendiente", "pagada", "enviada", "entregada", "cancelada"];

async function cargarOrdenes() {
  const tbody = document.getElementById("tabla-ordenes");
  try {
    const ordenes = await listarTodasLasOrdenes();
    if (!ordenes.length) {
      tbody.innerHTML = `<tr><td colspan="4" class="text-muted text-center py-3">No hay órdenes.</td></tr>`;
      return;
    }
    tbody.innerHTML = ordenes
      .map(
        (o) => `
      <tr>
        <td><small>${new Date(o.fecha).toLocaleString()}</small></td>
        <td><small>${o.items.map((i) => `${i.nombre_producto} ×${i.cantidad}`).join(", ")}</small></td>
        <td>$${o.total.toFixed(2)}</td>
        <td>
          <select class="form-select form-select-sm" onchange="cambiarEstado('${o.id}', this.value)">
            ${ESTADOS.map((e) => `<option value="${e}" ${e === o.estado ? "selected" : ""}>${e}</option>`).join("")}
          </select>
        </td>
      </tr>`,
      )
      .join("");
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="4" class="text-danger text-center py-3">${e.message}</td></tr>`;
  }
}

async function cambiarEstado(id, estado) {
  try {
    await actualizarEstadoOrden(id, estado);
  } catch (e) {
    alert("No se pudo cambiar el estado: " + e.message);
    cargarOrdenes();
  }
}

const ROLES = ["cliente", "operador", "admin"];

async function cargarUsuarios() {
  const tbody = document.getElementById("tabla-usuarios");
  try {
    const usuarios = await listarUsuarios();
    tbody.innerHTML = usuarios
      .map((u) => {
        const esAdminPrincipal = u.email === "admin@gmail.com";
        return `
      <tr>
        <td>${u.nombre}</td>
        <td>${u.email}</td>
        <td><span class="badge ${u.rol === "admin" ? "bg-success" : u.rol === "operador" ? "bg-info text-dark" : "bg-secondary"}">${u.rol}</span></td>
        <td>
          ${
            esAdminPrincipal
              ? `<span class="text-muted small">Admin principal</span>`
              : `<select class="form-select form-select-sm" style="max-width:160px" onchange="cambiarRol('${u.email}', this.value)">
                 ${ROLES.map((r) => `<option value="${r}" ${r === u.rol ? "selected" : ""}>${r}</option>`).join("")}
               </select>`
          }
        </td>
      </tr>`;
      })
      .join("");
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="4" class="text-danger text-center py-3">${e.message}</td></tr>`;
  }
}

async function cambiarRol(email, rol) {
  try {
    await cambiarRolUsuario(email, rol);
    cargarUsuarios();
  } catch (e) {
    alert("No se pudo cambiar el rol: " + e.message);
    cargarUsuarios();
  }
}

function conectarChatAdmin() {
  const WS_BASE = API_BASE.replace(/^http/, "ws");
  const socket = new WebSocket(`${WS_BASE}/ws/staff`);
  window._adminSocket = socket;

  socket.onmessage = (evento) => {
    const msg = JSON.parse(evento.data);
    if (msg.tipo === "escalamiento") {
      agregarEscalamiento(msg.conversacion_id, msg.cliente_id, msg.contenido);
    }
  };
}

function agregarEscalamiento(conversacionId, clienteId, contenido) {
  document.getElementById("chat-admin-vacio").classList.add("d-none");
  const lista = document.getElementById("chat-admin-lista");
  const col = document.createElement("div");
  col.className = "col-md-6";
  col.innerHTML = `
    <div class="card">
      <div class="card-body">
        <div class="small text-muted">Cliente: ${clienteId}</div>
        <p class="mb-2"><strong>“${contenido}”</strong></p>
        <div class="input-group input-group-sm">
          <input type="text" class="form-control" placeholder="Tu respuesta...">
          <button class="btn btn-brand">Responder</button>
        </div>
      </div>
    </div>`;
  const input = col.querySelector("input");
  const boton = col.querySelector("button");
  boton.addEventListener("click", () => {
    const texto = input.value.trim();
    if (!texto) return;
    window._adminSocket.send(
      JSON.stringify({ conversacion_id: conversacionId, contenido: texto }),
    );
    input.value = "";
    boton.textContent = "Enviado ✓";
    boton.disabled = true;
  });
  lista.prepend(col);
}

cargarProductos();
cargarOrdenes();
if (esAdmin) cargarUsuarios();
conectarChatAdmin();
