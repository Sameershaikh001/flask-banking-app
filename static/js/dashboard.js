document.addEventListener('DOMContentLoaded', async function() {
    try {
        console.log("Dashboard loaded – fetching profile...");
        const profile = await apiCall('/profile');
        console.log("Profile:", profile);

        const welcomeEl = document.getElementById('welcome-message');
        if (profile.role === 'admin') {
            welcomeEl.textContent = `Welcome, Admin ${profile.username}! 👋`;
        } else {
            welcomeEl.textContent = `Welcome back, ${profile.username}! 👋`;
        }

        // Fetch balance
        console.log("Fetching balance...");
        const balanceData = await apiCall('/balance');
        console.log("Balance data:", balanceData);

        const balanceEl = document.getElementById('balance');
        if (balanceEl) {
            balanceEl.textContent = `₹${balanceData.balance.toFixed(2)}`;
        } else {
            console.error("Balance element not found!");
        }

        // Show admin actions if role is admin
        if (profile.role === 'admin') {
            const adminActions = document.getElementById('admin-actions');
            if (adminActions) {
                adminActions.style.display = 'block';
                console.log("Admin actions shown");
            }
        }
    } catch (error) {
        console.error("Dashboard error:", error);
        alert('Failed to load dashboard: ' + error.message);
    }
});

// Deposit/Withdraw functions (unchanged)...
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