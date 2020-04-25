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
      $.ajax({
        type:'GET',
        url: "http://127.0.0.1:5000/", 
        dataType: 'json',
        data: {'query': input_query},
        crossDomain : true,
        // header:"Access-Control-Allow-Origin: http://127.0.0.1:5000/",

        success: function(result)
        { 
          console.log("response:"+JSON.stringify(result))
          $("#marathi").val(JSON.stringify(result));
      },
      error: function(err)
      {
        console.log("error message:"+JSON.stringify(err))
      }
    });
      
    });
});