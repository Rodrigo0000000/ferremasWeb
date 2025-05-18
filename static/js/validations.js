const form = document.getElementById('loginForm');
const username = document.getElementById('username');
const password = document.getElementById('password');
const userError = document.getElementById('user-error');
const passError = document.getElementById('pass-error');

form.addEventListener('submit', (e) => {
    e.preventDefault();

    let valid = true;

    if (username.value.trim().length < 3) {
    userError.style.display = 'block';
    valid = false;
    } else {
    userError.style.display = 'none';
    }

    if (
    password.value.trim().length < 6 ||
    password.value.trim().length > 12
    ) {
    passError.style.display = 'block';
    valid = false;
    } else {
    passError.style.display = 'none';
    }

    if (valid) {
        form.submit();
    }
});