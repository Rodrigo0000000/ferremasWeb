function initSidebarDropdowns() {
const sidebarButtons = document.querySelectorAll('.sidebar .dropdown-btn');
sidebarButtons.forEach((btn) => {
    btn.addEventListener('click', function () {
    this.classList.toggle('active');
    const container = this.nextElementSibling;
    container.style.display = container.style.display === 'block' ? 'none' : 'block';
    });
});
}

document.addEventListener('DOMContentLoaded', initSidebarDropdowns);

  let carrito = [];
  let total = 0;
  let carritoVisible = false;

  function agregarAlCarrito(id, nombre, precio) {
    carrito.push({ id, nombre, precio });
    total += parseFloat(precio);
    actualizarCarrito();
  }

  function actualizarCarrito() {
    const lista = document.getElementById("carrito-lista");
    const totalSpan = document.getElementById("carrito-total");
    lista.innerHTML = "";
    carrito.forEach(item => {
      const li = document.createElement("li");
      li.textContent = `${item.nombre} - $${item.precio}`;
      lista.appendChild(li);
    });
    totalSpan.textContent = total.toFixed(2);
  }

  function toggleCarrito() {
    carritoVisible = !carritoVisible;
    document.getElementById("carrito-dropdown").style.display = carritoVisible ? "block" : "none";
  }