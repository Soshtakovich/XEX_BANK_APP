document.addEventListener('DOMContentLoaded', function () {

    document.getElementById('logoutBtn').addEventListener('click', function () {
  
        sessionStorage.removeItem('user_id'); 
        sessionStorage.removeItem('user_name'); 
        sessionStorage.removeItem('user_surname'); 

        #console.log('User logged out');

        window.location.href = "/index_2";
    });
});

