const form = document.getElementById('loginForm');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const rememberMeCheckbox = document.getElementById('rememberMe');
const forgetPasswordLink = document.getElementById('forgetPasswordLink');
const forgetPasswordPopup = document.getElementById('forgetPasswordPopup');
const resetButton = document.getElementById('resetButton');
const closePopup = document.getElementById('closePopup');
const resetEmail = document.getElementById('resetEmail');
const emailError = document.getElementById('emailError');

window.onload = () => {
    const savedUsername = localStorage.getItem('username');
    const savedPassword = localStorage.getItem('password');
    const rememberMe = localStorage.getItem('rememberMe') === 'true';

    if (rememberMe) {
        usernameInput.value = savedUsername;
        passwordInput.value = savedPassword;
        rememberMeCheckbox.checked = true;
    }
};

form.addEventListener('submit', (e) => {
    let isValid = true;
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    usernameInput.style.borderColor = '';
    passwordInput.style.borderColor = '';
    
    if (username === '' || username.length < 3) {
        alert('❌ Username must be at least 3 characters long!');
        usernameInput.style.borderColor = 'red';
        isValid = false;
    }

    if (password === '' || password.length < 6) {
        alert('❌ Password must be at least 6 characters long!');
        passwordInput.style.borderColor = 'red';
        isValid = false;
    }

    if (!isValid) {
        e.preventDefault();
    } else {
        if (rememberMeCheckbox.checked) {
            localStorage.setItem('username', username);
            localStorage.setItem('password', password);
            localStorage.setItem('rememberMe', true);
        } else {
            localStorage.removeItem('username');
            localStorage.removeItem('password');
            localStorage.setItem('rememberMe', false);
        }
        alert('✅ Login successful!');
    }
});

forgetPasswordLink.addEventListener('click', (e) => {
    e.preventDefault();
    forgetPasswordPopup.style.display = 'block';
});

closePopup.addEventListener('click', () => {
    forgetPasswordPopup.style.display = 'none';
});

resetButton.addEventListener('click', () => {
    const email = resetEmail.value.trim();
    
    // Validate if the email contains "@"
    if (email === '' || !email.includes('@')) {
        emailError.style.display = 'block'; // Show error message
    } else {
        emailError.style.display = 'none'; // Hide error message
        alert(`✅ Reset link has been sent to ${email}`);
        forgetPasswordPopup.style.display = 'none';
    }
});
