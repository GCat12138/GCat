/*
	Author: yuanzm
	lastEditDate: 2014-08-10
	description: This Javascript document is mean to complete the function
	of form verify.the Object formVerify comtains methods of verify the form
	of regist.If you want to extend it,please make sure that the content you
	add has the common style.
*/


(function() {
  $(function() {
    var formVerify, loginVerify, trim, verifyPhone;
    $(".last-step").click(function() {
      return formVerify.init();
    });
    $(".commit").click(function() {
      return loginVerify.init();
    });
    formVerify = {
      init: function() {
        $(".tips").text("");
        if (this.verify()) {
          return this.ajaxPost();
        }
      },
      verify: function() {
        var password, phoneNum, verification;
        phoneNum = $("#phoneNumber");
        password = $("#password");
        verification = $("#verification");
        if (!verifyPhone(phoneNum.val())) {
          phoneNum.focus().next().text("手机格式错误");
          return false;
        }
        if (password.val().length === 0) {
          password.focus().next().text("请输入密码");
          return false;
        }
        if (verification.val().length === 0) {
          verification.focus().next().text("请输入验证码");
          return false;
        }
        return true;
      },
      ajaxPost: function() {
        var form;
        form = $("#register_form").serialize();
        return $.post("/register", form, function(data) {
          var registTips, success;
          success = data.success;
          registTips = $(".last-step").next();
          if (success === 1) {
            history.go(0);
          }
          if (success === 0) {
            registTips.text("注册失败，请再试一次");
          }
          if (success === 2) {
            return registTips.text("您已注册，请直接登陆");
          }
        });
      }
    };
    loginVerify = {
      init: function() {
        $(".tips").text("");
        if (this.verify()) {
          return this.ajaxLogin();
        }
      },
      verify: function() {
        var password, phoneNum;
        phoneNum = $("#phoneNumbaer");
        password = $("#loginpassword");
        if (!verifyPhone(phoneNum.val())) {
          phoneNum.focus().next().text("手机格式错误");
          return false;
        }
        if (password.val().length === 0) {
          password.focus().next().text("请输入密码");
          return false;
        }
        return true;
      },
      ajaxLogin: function() {
        var form, loginTips;
        form = $("#loginForm").serialize();
        loginTips = $(".commit").next();
        return $.post("/login", form, function(data) {
          var success;
          success = data.success;
          if (success === 1) {
            history.go(0);
          }
          if (success === 0) {
            return loginTips.text("用户账号密码错误或者该用户不存在");
          }
        });
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
