$(document).ready(function() {
    $('#register').submit(function(event) { 
        event.preventDefault();
        var name = $('#name').val();
        var email = $('#email').val();
        var phone_number = $('#phone-number').val();
        var password = $('#password').val();
        var confirm_password = $('#confirm-password').val();

        console.log("password: ", password);
        console.log("confirm_password: ", confirm_password);

        if (password != confirm_password) {
            alert('Passwords do not match');
            return;
        }

        $.ajax({
            url: '/register',
            type: 'POST',
            data: {
                'name': name,
                'email': email,
                'phone_number': phone_number,
                'password': password,
                'confirm_password': confirm_password
            },
            success: function(response) {
                window.location.href = '/login';
            },
            error: function(error) {
                alert('An error occurred while registering. Please try again later.');
                console.log(error);
            }
        });
    });
});

