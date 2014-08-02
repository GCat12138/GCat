$(document).ready(function(){
  bindButtons();
});

function bindButtons()
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
