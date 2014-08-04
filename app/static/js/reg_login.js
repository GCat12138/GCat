$(document).ready(function(){
  setUp();
  phoneNumberCheck();
});

function setUp()
{
  $("#reg_login").find("[name='t_reg_btn']").click( regButton );
  $("#reg_login").find("[name='t_log_btn']").click( logButton );
}

function regButton()
{
  show_hide_forms(1, 0);
}

function logButton()
{
  show_hide_forms(0, 1);
}

function show_hide_forms(reg, login)
{
  if (reg == 1) {
    $("#reg_login").find("[id='register_form']").css("display", "block");
  } else {
    $("#reg_login").find("[id='register_form']").css("display", "none");
  }

  if ( login == 1 ){
    $("#reg_login").find("#loginForm").css("display", "block");
  } else {
    $("#reg_login").find("#loginForm").css("display", "none");
  }
}

function phoneNumberCheck()
{
  var phoneNumberInput = $("#register_form").find("[name='phoneNumber']");
  $(phoneNumberInput).blur(function(){
    var phoneNumber = $(phoneNumberInput).val();
    var url = 'check_phoneNumber/' + phoneNumber;
    if ( phoneNumber.length == 11 ){
      $.get(url, function(data, status){
        if( status == "success"){
          if ( data == '1'){
            //phoneNumber exists
            var msg = "<span id='phoneCheck' style='color:red'>该手机号已存在，请直接登录</span>" ;
            $("#register_form").find("#phoneCheck").remove();
            $("#register_form").prepend(msg);
            $("#get_v_code_btn").attr("disabled", "true");
          } else {
            $("#get_v_code_btn").removeAttr("disabled");
          }
        }
      });
    }
  });
}
