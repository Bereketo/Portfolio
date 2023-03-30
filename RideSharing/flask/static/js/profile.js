/*$(document).ready(function() {
    $.ajax({
        url: '/profile',
        type: 'GET',
        success: function(response) {
            $('#name').text(response.name);
            $('#email').text(response.email);
            $('#phone').text(response.phone_number);
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log(xhr.responseText);
        }
    });
});
*/

$(document).ready(function() {
  $.getJSON('/profile', function(data) {
    $('#name').text(data.name);
    $('#email').text(data.email);
    $('#phone').text(data.phone_number);
  });

  $('.EditProfile').click(function() {
    window.location.href = "/editProfile";
  });

  $('.OrderRide').click(function() {
    window.location.href = "/book";
  });
});

