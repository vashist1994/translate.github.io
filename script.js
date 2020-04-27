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
      var input_query = $("#fullName").val()
      console.log("input query data:"+ input_query)
      var settings = {
        "url": "http://localhost:5000/"+input_query,
        "method": "GET",
        "timeout": 0,
      };
      $.ajax(settings).done(function (response) {
        $("#marathi").val(JSON.stringify(response['Marathi Sentance'])).css("color","black")
        console.log(JSON.stringify(response));
      });
          
    });
});