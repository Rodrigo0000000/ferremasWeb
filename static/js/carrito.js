function comprar() {
  if (carrito.length === 0) {
    alert("El carrito está vacío");
    return;
  }

  fetch('/comprar', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ productos: carrito })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert("Compra realizada con éxito");
      carrito = [];
      total = 0;
      actualizarCarrito();
      toggleCarrito(); // opcional para ocultar
    } else {
      alert("Error al procesar la compra");
    }
  });
}