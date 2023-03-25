$(document).ready(function() {
    var user = JSON.parse($('#user-data').text());
    $('#user-email').text(user.email);
    $('#user-name').text(user.name);
    $('#user-age').text(user.age);
});

