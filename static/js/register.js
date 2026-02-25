document.getElementById('registerForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const messageDiv = document.getElementById('message');
    
    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });
        const data = await response.json();
        if (response.ok) {
            messageDiv.style.display = 'block';
            messageDiv.className = 'alert alert-success';
            messageDiv.textContent = 'Registration successful! Redirecting to login...';
            setTimeout(() => {
                window.location.href = '/login-page';
            }, 2000);
        } else {
            messageDiv.style.display = 'block';
            messageDiv.className = 'alert alert-error';
            messageDiv.textContent = data.message || 'Registration failed';
        }
    } catch (error) {
        messageDiv.style.display = 'block';
        messageDiv.className = 'alert alert-error';
        messageDiv.textContent = 'Network error';
    }
});