document.addEventListener('DOMContentLoaded', async function() {
    try {
        // Fetch balance
        const data = await apiCall('/balance');
        document.getElementById('balance').textContent = `₹${data.balance.toFixed(2)}`;
        
        // Fetch user profile to check role
        const profile = await apiCall('/profile');
        if (profile.role === 'admin') {
            document.getElementById('admin-actions').style.display = 'block';
        }
    } catch (error) {
        alert('Failed to load dashboard: ' + error.message);
    }
});

// Deposit form
function showDepositForm() {
    document.getElementById('deposit-form').style.display = 'block';
}
function hideDepositForm() {
    document.getElementById('deposit-form').style.display = 'none';
}
document.getElementById('depositForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    const amount = parseFloat(document.getElementById('deposit-amount').value);
    try {
        const data = await apiCall('/deposit', 'POST', { amount });
        alert('Deposit successful! New balance: ₹' + data.new_balance);
        location.reload();
    } catch (error) {
        alert('Deposit failed: ' + error.message);
    }
});

// Withdraw form
function showWithdrawForm() {
    document.getElementById('withdraw-form').style.display = 'block';
}
function hideWithdrawForm() {
    document.getElementById('withdraw-form').style.display = 'none';
}
document.getElementById('withdrawForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    const amount = parseFloat(document.getElementById('withdraw-amount').value);
    try {
        const data = await apiCall('/withdraw', 'POST', { amount });
        alert('Withdrawal successful! New balance: ₹' + data.new_balance);
        location.reload();
    } catch (error) {
        alert('Withdrawal failed: ' + error.message);
    }
});