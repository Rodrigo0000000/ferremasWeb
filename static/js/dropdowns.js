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