(function() {
  $(function() {
    return $(".no-login-button").click(function() {
      return $("html,body").animate({
        scrollTop: "1800px"
      }, 400);
    });
  });

}).call(this);
