$ ->
	initPage = ->
		pageWidth = window.screen.availWidth
		$("header").css "left",(pageWidth - 990) / 2

	initScroll = ->
		$("header li").click ->
			tempObj = $(this)
			indexVal = tempObj.index() + 1;
	initPage();
	initScroll();


	#点击菜单更改对应的背景图片
	$("header li").click ->
		tempObj = $ this
		tempPic = tempObj.find "img"
		indexVal = tempObj.index() + 1
		$.each $("header li").not(".without"), ->
			temp = $(this)
			picVal = temp.index() + 1
			temp.find("img").attr "src", "static/images/header/menu" + picVal + ".png"
		tempPic.attr "src","static/images/header/menu" + indexVal + "-2.png"
	#点击注册和登陆按钮的效果
	$(".reg-btn").click ->
		tempObj = $(this)
		loginBtn = $(".login-btn")
		tempObj.css "background","../images/part4/reg-bg.png"
		loginBtn.css "background","../images/part4/login-before-bg.png"
	$(".login-btn").click ->
		tempObj = $(this)
		regBtn = $(".reg-btn")
		tempObj.css "background","../images/part4/login-bg.png"
		regBtn.css "background","../images/part4/reg-bg-before.png"
