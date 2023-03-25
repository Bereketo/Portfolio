$(document).ready(function() {
    $('#login-form').submit(function(event) {
        event.preventDefault();
        var formdata = $(this).serialize();
        $.post('/login', formdata, function(response) {
            if (response.success) {
                // Redirect to the user's profile page
                window.location.href = '/profile?user=' + JSON.stringify(response.user);
            } else {
                // Display an error message
                alert(response.message);
            }
        });
    });
});

