const dropdowns = document.querySelectorAll('.dropdown-btn');
dropdowns.forEach(btn => {
    btn.addEventListener('click', () => {
    btn.classList.toggle('active');
    const container = btn.nextElementSibling;
    if (container.style.display === 'block') {
        container.style.display = 'none';
    } else {
        container.style.display = 'block';
    }
    });
});

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

// Llamar a la función cuando cargue la página
document.addEventListener('DOMContentLoaded', initSidebarDropdowns);