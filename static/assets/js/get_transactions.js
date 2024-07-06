function fetchTransactions() {
    fetch('/get_transactions')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayTransactions(data.transactions);
            } else {
                console.error('Failed to fetch transactions:', data.message);
            }
        })
        .catch(error => console.error('Error fetching transactions:', error));
}

function displayTransactions(transactions) {
    const tableBody = document.getElementById('transactions-table-body');
    tableBody.innerHTML = ''; // Clear previous data

    transactions.forEach(transaction => {
        const row = document.createElement('tr');
        
        const transactionIdCell = document.createElement('td');
        transactionIdCell.textContent = transaction.transaction_id;
        row.appendChild(transactionIdCell);

        const accountTypeCell = document.createElement('td');
        accountTypeCell.textContent = transaction.account_type;
        row.appendChild(accountTypeCell);

        const transactionTypeCell = document.createElement('td');
        transactionTypeCell.textContent = transaction.transaction_type;
        row.appendChild(transactionTypeCell);

        const amountCell = document.createElement('td');
        amountCell.textContent = 'R ' + transaction.amount;  // Concatenate 'R ' with amount
        row.appendChild(amountCell);
        
        const descriptionCell = document.createElement('td');
        descriptionCell.textContent = transaction.description;
        row.appendChild(descriptionCell);

        const transactionDateCell = document.createElement('td');
        transactionDateCell.textContent = transaction.transaction_date;
        row.appendChild(transactionDateCell);

        tableBody.appendChild(row);
    });
}

// Call fetchTransactions when the page loads or as needed
document.addEventListener('DOMContentLoaded', function() {
    fetchTransactions();
});
