document.addEventListener('DOMContentLoaded', function () {
    const userId = sessionStorage.getItem('user_id');
    const userName = sessionStorage.getItem('user_name');
    const userSurname = sessionStorage.getItem('user_surname');

    if (userId && userName && userSurname) {
        document.getElementById('user-name').textContent = `${userName} ${userSurname}`;
    } else {
        if (!userId) {
            #console.error('User ID not found in session storage');
            return;
        }

        function updateUserName() {
            fetch(`/get_user_info?user_id=${userId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        #console.error('Error:', data.error);
                    } else {
                        document.getElementById('user-name').textContent = `${data.name_s} ${data.surname}`;
                        sessionStorage.setItem('user_name', data.name_s);
                        sessionStorage.setItem('user_surname', data.surname);
                    }
                })
                .catch(error => console.error('Error fetching user info:', error));
        }

        function updateAccountBalances() {
            fetch(`/get_accounts?user_id=${userId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        #console.error('Error:', data.error);
                    } else {
                        data.forEach(account => {
                            if (account.account_type === 'Debit') {
                                document.getElementById('debit-bal1').textContent = account.available_balance;
                                document.getElementById('debit-bal2').textContent = account.balance;
                                document.getElementById('debit-bal22').textContent = account.balance;
                            } else if (account.account_type === 'Savings') {
                                document.getElementById('savings-bal1').textContent = account.available_balance;
                                document.getElementById('savings-bal2').textContent = account.balance;
                                document.getElementById('savings-bal22').textContent = account.balance;
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

       updateUserName();
        updateAccountBalances();
    }
});
