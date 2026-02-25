let currentPage = 1;
let perPage = 10;
let totalPages = 1;

async function loadTransactions(page = 1) {
    try {
        const data = await apiCall(`/transactions?page=${page}&per_page=${perPage}`);
        displayTransactions(data.transactions);
        totalPages = data.pagination.pages;
        document.getElementById('pageInfo').textContent = `Page ${data.pagination.page} of ${totalPages}`;
        document.getElementById('prevPage').disabled = (data.pagination.page === 1);
        document.getElementById('nextPage').disabled = (data.pagination.page === totalPages);
        currentPage = data.pagination.page;
    } catch (error) {
        document.getElementById('transaction-list').innerHTML = '<tr><td colspan="6">Failed to load transactions</td></tr>';
    }
}

function displayTransactions(transactions) {
    const tbody = document.getElementById('transaction-list');
    if (transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6">No transactions found</td></tr>';
        return;
    }
    let html = '';
    transactions.forEach(tx => {
        const date = new Date(tx.timestamp).toLocaleString();
        const other = tx.to || tx.from;
        html += `<tr>
            <td>${tx.id}</td>
            <td>${tx.type}</td>
            <td>${other}</td>
            <td>₹${tx.amount.toFixed(2)}</td>
            <td>${tx.description || '-'}</td>
            <td>${date}</td>
        </tr>`;
    });
    tbody.innerHTML = html;
}

document.getElementById('prevPage').addEventListener('click', () => {
    if (currentPage > 1) loadTransactions(currentPage - 1);
});
document.getElementById('nextPage').addEventListener('click', () => {
    if (currentPage < totalPages) loadTransactions(currentPage + 1);
});
document.getElementById('perPage').addEventListener('change', (e) => {
    perPage = parseInt(e.target.value);
    loadTransactions(1);
});

// Initial load
loadTransactions();