document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.querySelector('.login-form');
  const errorMessage = document.createElement('p');
  errorMessage.id = 'login-error';
  errorMessage.style.color = 'red';
  loginForm.appendChild(errorMessage);

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        });

        if (response.ok) {
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = 'index.html';
        } else {
          const errorText = await response.text();
          errorMessage.textContent = 'Login failed: ' + errorText;
        }
      } catch (error) {
        errorMessage.textContent = 'Network error: ' + error.message;
      }
    });
  }
});
