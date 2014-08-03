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
  var s_hour = parseInt( $("#s_hour").text() );
  var s_minute = parseInt( $("#s_minute").text() );
  var s_second = parseInt( $("#s_second").text() );
  var totalSeconds = s_hour * 3600 + s_minute * 60 + s_second * 1;
  if (totalSeconds > 0) {
    totalSeconds = totalSeconds - 1;
    $("#s_hour").text( Math.floor(totalSeconds / 3600 ) );
    totalSeconds = totalSeconds % 3600;
    $("#s_minute").text( Math.floor(totalSeconds / 60) );
    totalSeconds = totalSeconds % 60;
    $("#s_second").text( totalSeconds );
  } else {
    // start to get the meal
    $(".getButton").css("display", "block");
  }

  var e_hour = parseInt( $("#e_hour").text() );
  var e_minute = parseInt( $("#e_minute").text() );
  var e_second = parseInt( $("#e_second").text() );
  var e_totalSeconds = e_hour * 3600 + e_minute * 60 + e_second* 1;

  if (e_totalSeconds > 0) {
    e_totalSeconds = e_totalSeconds - 1;
    $("#e_hour").text( Math.floor(e_totalSeconds / 3600 ) );
    e_totalSeconds = e_totalSeconds % 3600;
    $("#e_minute").text( Math.floor(e_totalSeconds / 60) );
    e_totalSeconds = e_totalSeconds % 60;
    $("#e_second").text( e_totalSeconds );
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
  $("#get_v_code_btn").click( GetVerificationCodeFunction );
}

function loginFunction()
{
//  $("#loginForm").submit();
  $.post(
    '/login',
    $("#loginForm").serialize(),
    function( data, status ){
      if (status == 'success' && data == '1' ) {
        window.location.href = "/index";
      } else {
        alert("failed");
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
      if ( status =='success' && data == '1') {
        window.location.href = "/";
      } else {
        alert( data + " " +  "failed" );
      }
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
      if (status == "success" && data == "1") {
        var oldLikes = $("#likes").text();
        $("#likes").text( parseInt(oldLikes) + 1 );
        $("#mealLike").remove();
      }
    }
  );
}

function getMealAfterLoginFunction()
{
  $("#get_meal_confirm_form").css("display", "block");
//  $("#get_meal_after_login").css("display", "none");
  $("#get_meal_after_login").remove();
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
//  $("#get_meal_without_login").css("display", "none");
  $("#get_meal_without_login").remove();
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

function GetVerificationCodeFunction()
{
  var phoneNumber = $("#get_v_code_btn").parent().find("[name='phoneNumber']").val();
  if (phoneNumber.length == 11) {
    phoneNumber = parseInt( phoneNumber );

    $("#get_v_code_btn").attr("disabled", "true");
    // get the verification code
    $.post(
      "/sms",
      {
        "phoneNumber":phoneNumber
      },
      function( data, status ){
      }
    );

  } else {
    alert("手机号码应该是11位");
  }

}
