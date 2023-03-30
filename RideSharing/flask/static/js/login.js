$(document).ready(function() {
    $('#login').submit(function(event) { 
        event.preventDefault();
        var email = $('#email').val();
        var password = $('#password').val();

        $.ajax({
            url: '/login',
            type: 'POST',
            data: {
                'email': email,
                'password': password
            },
            success: function(response) {
                if (response.redirect) {
                    window.location.href = response.redirect;
                } else {
                    $('#error').text("Incorrect credentials").css("color", "red");
                }
            },
		
            error: function(error) {
                   $("#error").text("Incorret username or password")
            }


        });
    });
});

