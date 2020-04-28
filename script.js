$( document ).ready(function(){

    $(".dropdown-button").dropdown();
    $(".button-collapse").sideNav();

    $('a[href*="#"]:not([href="#"])').click(function() {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
          var target = $(this.hash);
          target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
          if (target.length) {
            $('html,body').animate({
              scrollTop: target.offset().top
            }, 1000);
            return false;
          }
        }
      });
    


    $(".request").click(function(){
      // input_value = $("fullName").val()
      if($.trim($('#fullName').val()) == ''){
        var toastHTML = '<span class="toast-span">Enter the sentance</span>';
        M.toast({html: toastHTML,displayLength:1500});
      }
      else {
        var input_query = $("#fullName").val()
        console.log("input query data:"+ input_query)
        $(".request").css("display","none")
        $(".spin-loader").css('display','inline-block')
        $("#marathi").val('')
        var settings = {
          "url": "https://eng-mar-translate.herokuapp.com/"+input_query,
          "method": "GET",
          "timeout": 0,
        };
        $.ajax(settings).done(function (response) {
          $(".spin-loader").css('display','none')
          $(".request").css("display","initial")
          $("#marathi").val(JSON.stringify(response['Marathi Sentance'])).css("color","black")
          console.log(JSON.stringify(response));
        }).fail(function(response){
          $("#marathi").val(JSON.stringify(response['Marathi Sentance'])).css("color","black")
          $(".spin-loader").css('display','none')
          $(".request").css("display","initial")
          // M.toast({html: 'I am a toast!'})
  
        });

      }    
    });
});