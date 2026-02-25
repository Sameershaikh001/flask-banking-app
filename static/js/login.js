document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const messageDiv = document.getElementById('message');
    
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (response.ok) {
            // Store token
            localStorage.setItem('access_token', data.access_token);
            // Redirect to dashboard
            window.location.href = '/dashboard';
        } else {
            messageDiv.style.display = 'block';
            messageDiv.className = 'alert alert-error';
            messageDiv.textContent = data.message || 'Login failed';
        }
    } catch (error) {
        messageDiv.style.display = 'block';
        messageDiv.className = 'alert alert-error';
        messageDiv.textContent = 'Network error';
    }
});