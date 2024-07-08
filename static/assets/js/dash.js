document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('transfer-btn').addEventListener('click', (event) => {
        showContent(event, 'transfer');
    });

    document.getElementById('withdraw-btn').addEventListener('click', (event) => {
        showContent(event, 'withdraw');
    });
});
