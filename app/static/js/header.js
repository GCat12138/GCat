(function() {
  $(function() {
    var page;
    page = {
      init: function() {
        return this.initPage();
      },
      initPage: function() {
        var pageWidth;
        pageWidth = window.innerWidth;
        if (typeof pageWidth !== "number") {
          if (document.compactMode === "CSS1Compact") {
            pageWidth = document.documentElement.clientWidth;
          } else {
            pageWidth = document.body.clientWidth;
          }
        }
        return $("#header").css("left", (pageWidth - 990) / 2);
      }
    };
    page.init();
    $(window).resize(function() {
      return page.init();
    });
    $("#header li").not(".without").click(function() {
      var htmlContent, indexVal, tempObj, topArray;
      tempObj = $(this);
      indexVal = tempObj.index();
      htmlContent = $("html,body");
      topArray = ["0px", "390px", "1120px", "1740px"];
      return htmlContent.animate({
        scrollTop: topArray[indexVal]
      }, 400);
    });
    $(".reg-btn").click(function() {
      var loginBtn, tempObj;
      tempObj = $(this);
      loginBtn = $(".login-btn");
      tempObj.css("background", "url(/static/images/part4/reg-bg.png)");
      return loginBtn.css("background", "url(/static/images/part4/login-before-bg.png)");
    });
    $(".login-btn").click(function() {
      var regBtn, tempObj;
      tempObj = $(this);
      regBtn = $(".reg-btn");
      tempObj.css("background", "url(/static/images/part4/login-bg.png)");
      return regBtn.css("background", "url(/static/images/part4/reg-bg-before.png)");
    });
    return $(window).scroll(function() {
      var i, indexVal, item, tempPic, top, topArray, _i, _len, _results;
      top = $(window).scrollTop();
      topArray = [0, 390, 1120, 1740];
      _results = [];
      for (i = _i = 0, _len = topArray.length; _i < _len; i = ++_i) {
        item = topArray[i];
        if (top - 50 <= item && item <= top + 50) {
          indexVal = i + 1;
          tempPic = $("#header li").not(".without").eq(i).find("img");
          $.each($("#header li").not(".without"), function(n) {
            var picVal, temp;
            if (n !== indexVal - 1) {
              temp = $(this);
              picVal = temp.index() + 1;
              return temp.find("img").attr("src", "/static/images/header/menu" + picVal + ".png");
            }
          });
          _results.push(tempPic.attr("src", "/static/images/header/menu" + indexVal + "-2.png"));
        } else {
          _results.push(void 0);
        }
      }
      return _results;
    });
  });

}).call(this);
