// Function to update user name from session or fetch if not available
function updateUserName() {
    const userId = sessionStorage.getItem('user_id');
    const userName = sessionStorage.getItem('user_name');
    const userSurname = sessionStorage.getItem('user_surname');

    if (userId && userName && userSurname) {
        document.getElementById('user-name').textContent = `${userName} ${userSurname}`;
    } else {
        if (!userId) {
            console.error('User ID not found in session storage');
            return;
        }

        fetch(`/get_user_info?user_id=${userId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Error:', data.error);
                } else {
                    document.getElementById('user-name').textContent = `${data.name_s} ${data.surname}`;
                    sessionStorage.setItem('user_name', data.name_s);
                    sessionStorage.setItem('user_surname', data.surname);
                }
            })
            .catch(error => console.error('Error fetching user info:', error));
    }
}

// Function to update account balances after transactions
function updateAccountBalances() {
    const userId = sessionStorage.getItem('user_id');

    fetch(`/get_accounts?user_id=${userId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
            } else {
                data.forEach(account => {
                    if (account.account_type === 'Debit') {
                        document.getElementById('debit-bal1').textContent = account.available_balance;
                        document.getElementById('debit-bal2').textContent = account.balance;
                    } else if (account.account_type === 'Savings') {
                        document.getElementById('savings-bal1').textContent = account.available_balance;
                        document.getElementById('savings-bal2').textContent = account.balance;
                    } else if (account.account_type === 'Credit') {
                        document.getElementById('credit-bal1').textContent = account.available_balance;
                        document.getElementById('credit-bal2').textContent = account.balance;
                    } else if (account.account_type === 'Investment') {
                        document.getElementById('invest-bal1').textContent = account.available_balance;
                        document.getElementById('invest-bal2').textContent = account.balance;
                    }
                });
            }
        })
        .catch(error => console.error('Error fetching account balances:', error));
}

// Event listeners for transaction buttons
document.addEventListener('DOMContentLoaded', function () {
    updateUserName();
    updateAccountBalances();
});

function handleTransfer() {
    const fromAccount = document.getElementById('transferDropdownFrom').value;
    const toAccount = document.getElementById('transferDropdownTo').value;
    const amount = parseFloat(document.getElementById('transferAmount').value);

    if (!fromAccount || !toAccount || isNaN(amount)) {
        alert('Please fill in all fields');
        return;
    }

    fetch('/transfer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ fromAccount, toAccount, amount })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Transfer successful');
            location.reload();  // Reload the page on success
        } else {
            alert(data.message || 'Transfer failed');
        }
    })
    .catch(error => {
        alert('An error occurred while processing your request.');
    });
}

function handleWithdraw() {
    const fromAccount = document.getElementById('withdrawDropdownFrom').value;
    const amount = parseFloat(document.getElementById('withdrawAmount').value);

    if (!fromAccount || isNaN(amount)) {
        alert('Please fill in all fields');
        return;
    }

    fetch('/withdraw', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ fromAccount, amount })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const code = data.withdrawalCode; // Assuming the response includes a withdrawal code
            alert(`Withdrawal successful. Your withdrawal code is: ${code}`);
            location.reload();  // Reload the page on success
        } else {
            alert(data.message || 'Withdrawal failed');
        }
    })
    .catch(error => {
        alert('An error occurred while processing your request.');
    });
}
