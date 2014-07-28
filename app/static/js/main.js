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
  var now_cnt =  parseInt( $("#count").text() );
  now_cnt += 1;
  $("#count").text( now_cnt );
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
