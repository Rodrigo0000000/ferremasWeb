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