document.getElementById('transferForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const to_username = document.getElementById('to_username').value;
    const amount = parseFloat(document.getElementById('amount').value);
    const description = document.getElementById('description').value;
    const messageDiv = document.getElementById('message');

    try {
        const data = await apiCall('/transfer', 'POST', { to_username, amount, description });
        messageDiv.style.display = 'block';
        messageDiv.className = 'alert alert-success';
        messageDiv.textContent = `Transfer successful! New balance: ₹${data.new_balance}`;
        setTimeout(() => {
            window.location.href = '/dashboard';
        }, 2000);
    } catch (error) {
        messageDiv.style.display = 'block';
        messageDiv.className = 'alert alert-error';
        messageDiv.textContent = error.message || 'Transfer failed';
    }
});