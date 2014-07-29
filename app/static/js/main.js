$(document).ready(function(){
  //csrf for ajax
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  // bind all buttons
  bindButtons();

  setInterval(countFunction, 1000);
  countFunction();
});

function countFunction()
{
  var hour = parseInt( $("#c_hour").text() );
  var minute = parseInt( $("#c_minute").text() );
  var second = parseInt( $("#c_second").text() );
  var totalSeconds = hour * 3600 + minute * 60 + second * 1;
  if (totalSeconds > 0) {
    totalSeconds = totalSeconds - 1;
    $("#c_hour").text( Math.floor(totalSeconds / 3600 ) );
    totalSeconds = totalSeconds % 3600;
    $("#c_minute").text( Math.floor(totalSeconds / 60) );
    totalSeconds = totalSeconds % 60;
    $("#c_second").text( totalSeconds );
  }
}

function bindButtons()
{
  $("#loginButton").click( loginFunction );
  $("#register_button").click( registerFunction );
  $("#mealLike").click( likeFunction );
  $("#get_meal_after_login").click( getMealAfterLoginFunction );
  $("#get_meal_confirm_button").click( getMealConfirmButton );
  $("#get_meal_without_login").click( getMealWithoutLoginFunction );
  $("#get_meal_without_log_confirm_button").click( getMealWithoutLoginConfirmFunction );
}

function loginFunction()
{
//  $("#loginForm").submit();

  $.post(
    '/login',
    $("#loginForm").serialize(),
    function( data, status ){
      if (status == 'success' ) {
        window.location.href = "/index";
      }
    }
  );
}

function registerFunction()
{
  $.post(
    '/register',
    $('#register_form').serialize(),
    function( data, status ){
      alert( data );
    }
  );
}

function likeFunction()
{
  mealId = $("#mealID").text();
  $.post(
    '/like',
    {
      mealId : mealId,
    },
    function( data, status ) {
      if (status == "success") {
        $("#likes").text(data);
      }
    }
  );
}

function getMealAfterLoginFunction()
{
  $("#get_meal_confirm_form").css("display", "block");
  $("#get_meal_after_login").css("display", "none");
}

function getMealConfirmButton()
{
  $.post(
    '/make_order',
    $("#get_meal_confirm_form").serialize(),
    function( data, status ){
      alert( data );
    }
  );
}

function getMealWithoutLoginFunction()
{
  $("#get_meal_without_log_form").css("display", "block");
  $("#get_meal_without_login").css("display", "none");
}

function getMealWithoutLoginConfirmFunction()
{
  alert('test');
  $.post(
    '/make_order',
    $("#get_meal_without_log_form").serialize(),
    function( data, status ){
      alert( status );
    }
  );
}
