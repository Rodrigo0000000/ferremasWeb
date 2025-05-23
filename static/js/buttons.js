document.addEventListener('DOMContentLoaded', () => {
    const loginButton = document.getElementById('loginID');
    if (loginButton) {
        loginButton.addEventListener('click', () => {
            window.location.href = '/login';
        });
    }

    const headerButton = document.getElementById('title');
    if (headerButton) {
        headerButton.addEventListener('click', () => {
            window.location.href = '/';
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('toggleSidebarBtn');
  const sidebar = document.getElementById('sidebar');

  toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('hidden');
  });
});
