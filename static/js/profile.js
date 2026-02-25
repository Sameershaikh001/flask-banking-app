document.addEventListener('DOMContentLoaded', async function() {
    try {
        const profile = await apiCall('/profile');
        document.getElementById('username').textContent = profile.username;
        document.getElementById('email').textContent = profile.email;
        document.getElementById('role').textContent = profile.role;
        document.getElementById('balance').textContent = `₹${profile.balance.toFixed(2)}`;
    } catch (error) {
        alert('Failed to load profile');
    }
});

document.getElementById('profileForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const newEmail = document.getElementById('new-email').value;
    const newPassword = document.getElementById('new-password').value;
    const body = {};
    if (newEmail) body.email = newEmail;
    if (newPassword) body.password = newPassword;
    
    if (Object.keys(body).length === 0) {
        alert('No changes to update');
        return;
    }
    
    try {
        const data = await apiCall('/profile', 'PUT', body);
        alert('Profile updated successfully');
        location.reload();
    } catch (error) {
        document.getElementById('message').style.display = 'block';
        document.getElementById('message').className = 'alert alert-error';
        document.getElementById('message').textContent = error.message || 'Update failed';
    }
});