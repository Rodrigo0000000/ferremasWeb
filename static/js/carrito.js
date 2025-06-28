function comprar() {
  if (carrito.length === 0) {
    alert("El carrito está vacío");
    return;
  }

  // Convertir carrito al formato esperado por el backend
  const productos = carrito.map(item => ({
    id: item.id,
    cantidad: item.cantidad
  }));

  fetch('/comprar', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ productos })
  })
  .then(response => response.json())
  .then(data => {
    console.log("Respuesta del servidor:", data);
    if (data.success) {
      alert(data.mensaje || "Compra realizada con éxito");
      carrito = [];
      total = 0;
      actualizarCarrito();
      toggleCarrito();
    } else {
      alert(data.error || "Error al procesar la compra");
    }
  })
  .catch(error => {
    console.error("Error en fetch:", error);
    alert("Error al procesar la compra");
  });
}
