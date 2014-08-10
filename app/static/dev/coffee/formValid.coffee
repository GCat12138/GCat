###
	Author: yuanzm
	lastEditDate: 2014-08-10
	description: This Javascript document is mean to complete the function
	of form verify.the Object formVerify comtains methods of verify the form
	of regist.If you want to extend it,please make sure that the content you
	add has the common style.
###
$ ->
	$(".last-step").click -> formVerify.init()
	$(".commit").click -> loginVerify.init()

	formVerify =
		init: ->
			#empty the tips text when click the commit button
			$(".tips").text("")
			if @.verify()
				@.ajaxPost()
		verify: ->
			phoneNum = $("#phoneNumber")
			password = $("#password")
			verification = $("#verification")
			if !verifyPhone(phoneNum.val())
				phoneNum.focus().next().text("手机格式错误")
				return false
			if password.val().length == 0
				password.focus().next().text("请输入密码")
				return false
			if verification.val().length == 0
				verification.focus().next().text("请输入验证码")
				return false
			return true
		ajaxPost: ->
			form = $("#register_form").serialize()
			$.post "/register", form,(data) ->
				success = data.success
				registTips = $(".last-step").next()
				if success == 1
					history.go(0)
				if success == 0
					registTips.text("注册失败，请再试一次")
				if success == 2
					registTips.text("您已注册，请直接登陆")

	loginVerify=
		init: ->
			$(".tips").text("")
			if @.verify()
				@.ajaxLogin()

		verify: ->
			phoneNum = $("#phoneNumbaer")
			password = $("#loginpassword")
			if !verifyPhone(phoneNum.val())
				phoneNum.focus().next().text("手机格式错误")
				return false
			if password.val().length == 0
				password.focus().next().text("请输入密码")
				return false
			return true
		ajaxLogin: ->
			form = $("#register_form").serialize()
			loginTips = $(".commit").next()
			$.post "/login", form, (data) ->
				success = data.success
				if success == 1
					history.go(0)
				if success == 0
					loginTips.text("用户账号密码错误或者该用户不存在")

	verifyPhone= (val)->
			re= /(^1[3|5|8][0-9]{9}$)/
			phone = trim(val)
			return re.test(val)
			
	trim= (str)-> str.replace(/^\s*|\s*$/g,"")


