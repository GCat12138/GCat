(function() {
  $(function() {
    var page;
    page = {
      init: function() {
        this.initPage();
        return this.initScroll();
      },
      initPage: function() {
        var pageWidth;
        pageWidth = window.screen.availWidth;
        return $("header").css("left", (pageWidth - 990) / 2);
      },
      initScroll: function() {
        return $("header li").not(".without").click(function() {
          var htmlContent, indexVal, tempObj, topArray;
          tempObj = $(this);
          indexVal = tempObj.index();
          htmlContent = $("html,body");
          topArray = ["0px", "400px", "1100px", "1800px"];
          return htmlContent.animate({
            scrollTop: topArray[indexVal]
          }, 400);
        });
      }
    };
    page.init();
    $("header li").click(function() {
      var indexVal, tempObj, tempPic;
      tempObj = $(this);
      tempPic = tempObj.find("img");
      indexVal = tempObj.index() + 1;
      $.each($("header li").not(".without"), function() {
        var picVal, temp;
        temp = $(this);
        picVal = temp.index() + 1;
        return temp.find("img").attr("src", "/static/images/header/menu" + picVal + ".png");
      });
      return tempPic.attr("src", "/static/images/header/menu" + indexVal + "-2.png");
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
      var i, item, tempPic, top, topArray, _i, _len, _results;
      top = $(window).scrollTop() + "px";
      topArray = ["0px", "400px", "1100px", "1800px"];
      _results = [];
      for (i = _i = 0, _len = topArray.length; _i < _len; i = ++_i) {
        item = topArray[i];
        if (item === top) {
          tempPic = $("header li").not(".without").eq(i).find("img");
          $.each($("header li").not(".without"), function() {
            var picVal, temp;
            temp = $(this);
            picVal = temp.index() + 1;
            return temp.find("img").attr("src", "/static/images/header/menu" + picVal + ".png");
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
