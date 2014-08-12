/*
	Author: yuanzm
	lastEditDate: 2014-08-10
	description: This Javascript document is mean to complete the function
	of form verify.
*/


(function() {
  $(function() {
    var forgotVerify, initPage, trim, verifyPhone;
    $("#submit").click(function() {
      return forgotVerify.init();
    });
    initPage = {
      init: function() {
        return $.each($("#header li").not(".without"), function() {
          var picVal, temp;
          temp = $(this);
          picVal = temp.index() + 1;
          return temp.find("img").attr("src", "/static/images/header/menu" + picVal + ".png");
        });
      }
    };
    initPage.init();
    forgotVerify = {
      init: function() {
        $(".tips").text("");
        return this.verify();
      },
      verify: function() {
        var flag, password, phoneNumber, verification;
        password = $("#password");
        phoneNumber = $("#phoneNumber");
        verification = $("#verification");
        flag = 0;
        if (!verifyPhone(phoneNumber.val())) {
          phoneNumber.focus().next().text("手机格式错误");
          flag++;
        }
        if (verification.val().length === 0) {
          verification.focus().next().text("请输入验证码");
          flag++;
        }
        if (password.val().length === 0) {
          password.focus().next().text("请输入新密码");
          flag++;
        }
        if (flag > 0) {
          return false;
        }
        return true;
      }
    };
    verifyPhone = function(val) {
      var phone, re;
      re = /(^1[3|5|8][0-9]{9}$)/;
      phone = trim(val);
      return re.test(val);
    };
    return trim = function(str) {
      return str.replace(/^\s*|\s*$/g, "");
    };
  });

}).call(this);
