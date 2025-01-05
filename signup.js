document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('signup-form').addEventListener('submit', function (e) {
      e.preventDefault();
  
      // Clear errors
      document.getElementById('username-error').textContent = '';
      document.getElementById('email-error').textContent = '';
      document.getElementById('password-error').textContent = '';
      document.getElementById('confirm-password-error').textContent = '';
  
      // Get user input
      const username = document.getElementById('username').value.trim();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;
      const confirmPassword = document.getElementById('confirm-password').value;
  
      let isValid = true;
  
      // Validate username
      if (!/^[a-zA-Z]+$/.test(username)) {
        document.getElementById('username-error').textContent = 'Username must contain letters only.';
        isValid = false;
      }
  
      // Validate email
      if (!email.includes('@')) {
        document.getElementById('email-error').textContent = 'Email must contain "@" symbol.';
        isValid = false;
      }
  
      // Validate password
      const passwordRegex = /^(?=.*[A-Z])(?=.*[a-zA-Z])(?=.*\d)[A-Za-z\d]{8,}$/;
      if (!passwordRegex.test(password)) {
        document.getElementById('password-error').textContent =
          'Password must be at least 8 characters long, contain at least one uppercase letter, and include both letters and numbers.';
        isValid = false;
      }
  
      // Confirm password
      if (password !== confirmPassword) {
        document.getElementById('confirm-password-error').textContent = 'Passwords do not match.';
        isValid = false;
      }
  
      // If valid, send data to backend
      if (isValid) {
        fetch('/signup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username,
            email,
            password,
            confirm_password: confirmPassword,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              alert(data.message);
              window.location.href = '/'; // Redirect on success
            } else {
              alert(data.message); // Show server error
            }
          })
          .catch((error) => {
            alert('An error occurred. Please try again.');
            console.error('Error:', error);
          });
      }
    });
  });
