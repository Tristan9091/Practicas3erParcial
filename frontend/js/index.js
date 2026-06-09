protegerPagina();

document.getElementById("usuario-email").textContent = obtenerEmail();
document.getElementById("btn-salir").addEventListener("click", cerrarSesion);

let productos = [];

async function cargarCatalogo() {
  try {
    productos = await listarProductos();
    renderCatalogo(productos);
  } catch (e) {
    alert("No se pudo cargar el catálogo: " + e.message);
  }
}

function renderCatalogo(lista) {
  const cont = document.getElementById("catalogo");
  const vacio = document.getElementById("catalogo-vacio");
  cont.innerHTML = "";

  vacio.classList.toggle("d-none", lista.length > 0);

  lista.forEach((p) => {
    const sinStock = p.stock <= 0;
    const col = document.createElement("div");
    col.className = "col-sm-6 col-md-4 col-lg-3";
    col.innerHTML = `
      <div class="card h-100 shadow-sm">
        <img src="${urlImagen(p.imagenes && p.imagenes[0])}" class="card-img-top producto-img" alt="${p.nombre}">
        <div class="card-body d-flex flex-column">
          <h5 class="card-title">${p.nombre}</h5>
          <p class="card-text text-muted small flex-grow-1">${p.descripcion || ""}</p>
          <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="fs-5 fw-bold text-brand">$${p.precio.toFixed(2)}</span>
            <span class="badge ${sinStock ? "bg-secondary" : "bg-success"}">
              ${sinStock ? "Agotado" : "Stock: " + p.stock}
            </span>
          </div>
          <button class="btn btn-brand btn-agregar" data-id="${p.id}" ${sinStock ? "disabled" : ""}>
            Agregar al carrito
          </button>
        </div>
      </div>`;
    cont.appendChild(col);
  });

  document.querySelectorAll(".btn-agregar").forEach((btn) => {
    btn.addEventListener("click", () => agregarAlCarrito(btn.dataset.id));
  });
}

document.getElementById("buscador").addEventListener("input", (e) => {
  const texto = e.target.value.toLowerCase().trim();
  const filtrados = productos.filter((p) =>
    p.nombre.toLowerCase().includes(texto),
  );
  renderCatalogo(filtrados);
});

function obtenerCarrito() {
  return JSON.parse(localStorage.getItem("carrito") || "[]");
}

function guardarCarrito(carrito) {
  localStorage.setItem("carrito", JSON.stringify(carrito));
  renderCarrito();
}

function agregarAlCarrito(productoId) {
  const producto = productos.find((p) => p.id === productoId);
  if (!producto) return;

  const carrito = obtenerCarrito();
  const existente = carrito.find((item) => item.id === productoId);

  if (existente) {
    if (existente.cantidad >= Number(producto.stock)) {
      alert("No hay más stock disponible de este producto");
      return;
    }
    existente.cantidad += 1;
  } else {
    carrito.push({
      id: producto.id,
      nombre: producto.nombre,
      precio: producto.precio,
      imagen: producto.imagenes && producto.imagenes[0],
      cantidad: 1,
    });
  }
  guardarCarrito(carrito);
}

function cambiarCantidad(productoId, delta) {
  const carrito = obtenerCarrito();
  const item = carrito.find((i) => i.id === productoId);
  if (!item) return;

  if (delta > 0) {
    const producto = productos.find((p) => p.id === productoId);
    if (producto && item.cantidad >= Number(producto.stock)) {
      alert("No hay más stock disponible de este producto");
      return;
    }
  }

  item.cantidad += delta;
  if (item.cantidad <= 0) {
    guardarCarrito(carrito.filter((i) => i.id !== productoId));
  } else {
    guardarCarrito(carrito);
  }
}

function quitarDelCarrito(productoId) {
  guardarCarrito(obtenerCarrito().filter((i) => i.id !== productoId));
}

function renderCarrito() {
  const carrito = obtenerCarrito();
  const cont = document.getElementById("carrito-items");
  const badge = document.getElementById("carrito-badge");
  const totalEl = document.getElementById("carrito-total");

  const totalItems = carrito.reduce((s, i) => s + i.cantidad, 0);
  badge.textContent = totalItems;
  badge.classList.toggle("d-none", totalItems === 0);

  if (carrito.length === 0) {
    cont.innerHTML = `<p class="text-muted text-center py-4">Tu carrito está vacío</p>`;
  } else {
    cont.innerHTML = carrito
      .map(
        (item) => `
      <div class="d-flex align-items-center gap-2 mb-3 border-bottom pb-2">
        <img src="${urlImagen(item.imagen)}" class="carrito-img" alt="${item.nombre}">
        <div class="flex-grow-1">
          <div class="small fw-bold">${item.nombre}</div>
          <div class="text-muted small">$${item.precio.toFixed(2)}</div>
          <div class="btn-group btn-group-sm mt-1">
            <button class="btn btn-outline-secondary" onclick="cambiarCantidad('${item.id}', -1)">−</button>
            <span class="btn btn-light disabled">${item.cantidad}</span>
            <button class="btn btn-outline-secondary" onclick="cambiarCantidad('${item.id}', 1)">+</button>
          </div>
        </div>
        <button class="btn btn-sm btn-outline-danger" onclick="quitarDelCarrito('${item.id}')">🗑️</button>
      </div>`,
      )
      .join("");
  }

  const total = carrito.reduce((s, i) => s + i.precio * i.cantidad, 0);
  totalEl.textContent = `$${total.toFixed(2)}`;
}

cargarCatalogo();
renderCarrito();
