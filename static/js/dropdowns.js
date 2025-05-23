document.addEventListener('DOMContentLoaded', () => {
  const dropdowns = document.querySelectorAll('.dropdown-btn');

  dropdowns.forEach(btn => {
    btn.addEventListener('click', () => {
      btn.classList.toggle('active');
      const container = btn.nextElementSibling;

      if (container.style.maxHeight) {
        container.style.maxHeight = null;
      } else {
        container.style.maxHeight = container.scrollHeight + "px";
      }
    });
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

document.addEventListener('DOMContentLoaded', initSidebarDropdowns);