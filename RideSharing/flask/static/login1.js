$(document).ready(function() {
  $("#login-button").click(function() {
    var email = $("#email").val();
    var password = $("#password").val();

    $.ajax({
      type: "POST",
      url: "/login",
      data: { email: email, password: password },
      success: function(data) {
        if (data.status == "success") {
          window.location.href = "/profile";
        } else {
          $("#error-message").text(data.message);
        }
      },
      error: function() {
        $("#error-message").text("An error occurred while processing your request. Please try again later.");
      }
    });
  });
});

