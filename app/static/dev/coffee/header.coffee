$ ->
	#init the page
	page=
		init: ->
			@.initPage()
		initPage: ->
			pageWidth = window.innerWidth
			if typeof pageWidth != "number"
				if document.compactMode == "CSS1Compact"
					pageWidth = document.documentElement.clientWidth
				else
					pageWidth = document.body.clientWidth
			$("#header").css "left",(pageWidth - 990) / 2
			
	page.init()

	$(window).resize ->
		page.init()
	
	$("#header li").not(".without").click ->
		tempObj = $(this)
		indexVal = tempObj.index()
		htmlContent = $("html,body")
		topArray = ["0px","390px","1120px","1740px"];
		htmlContent.animate({scrollTop: topArray[indexVal]},400)
		
	#点击注册和登陆按钮的效果
	$(".reg-btn").click ->
		tempObj = $(this)
		loginBtn = $(".login-btn")
		tempObj.css "background","url(/static/images/part4/reg-bg.png)"
		loginBtn.css "background","url(/static/images/part4/login-before-bg.png)"
	$(".login-btn").click ->
		tempObj = $(this)
		regBtn = $(".reg-btn")
		tempObj.css "background","url(/static/images/part4/login-bg.png)"
		regBtn.css "background","url(/static/images/part4/reg-bg-before.png)"

	$(window).scroll ->
		top = $(window).scrollTop()
		topArray = [0,390,1120,1740]
		for item, i in topArray
			if top - 50 <= item && item <= top + 50
				indexVal = i + 1;
				tempPic = $("#header li").not(".without").eq(i).find("img")
				$.each $("#header li").not(".without"), (n)->
					if n != indexVal - 1
						temp = $(this)
						picVal = temp.index() + 1
						temp.find("img").attr "src", "/static/images/header/menu" + picVal + ".png"
				tempPic.attr "src","/static/images/header/menu" + indexVal + "-2.png"
