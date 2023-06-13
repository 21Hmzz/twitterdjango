$(document).ready(function () {
  $(".subscrire").hide();
  $(".listefollow").hide();
  $(".listeFollower").hide();
  $('.popup_new_comment').hide();
  $("#searchBar").autocomplete({
    source: function (request, response) {
      $.ajax({
        url: "/search",
        type: "GET",
        data: request,
        success: function (data) {
          console.log(data);
          response($.map(data, function (item) {
            return {
              label: item.label,
              value: item.value,
              image: item.image,
              };
              })
              );
        },
      });
    },
    minLength: 1,
    select : function(event, ui){
      window.location.href = "/profil/"+ui.item.value;
    }
  })
  .autocomplete( "instance" )._renderItem = function( ul, item ) {
    if (item.image == null){
      item.image = "/static/erttiwtFront/img/defaut.jpg";
    }else{
      item.image = "/media/"+item.image;
    }
    return $( "<li class='searchresult' >" )
      .append( "<div class='searchresultdiv'><img src="+item.image+" style='width: 100px; height: 100px; border-radius: 50%; margin-right: 10px;'><div class='nameresult'><span>"+item.label+"</span><small>@"+item.label+"</small></div></div>" )
      .appendTo( ul );
  };

$("#showFollow").on("click", function () {
  $(".listefollow").show();
  $(".listeFollower").hide();


});

$("#showFollower").on("click", function () {
  $(".listeFollower").show();
  $(".listefollow").hide();

});
$(".message_item").animate({ scrollTop: $(".message_item").prop("scrollHeight")}, 100);
$("#message_field").each(function () {
  this.setAttribute("style", "height:" + (this.scrollHeight) + "px;overflow-y:hidden;");
}).on("input", function () {
  this.style.height = 0;
  this.style.height = (this.scrollHeight) + "px";
});

$(".comments").on("click", function () {
  
  var id = $(this).attr("id");

  var popup = $('#pop'+id);
  console.log(popup.attr("id"));

  if (popup.attr("id") == ('pop'+id)){
    popup = $('#pop'+id);
    if (popup.is(":visible")){
      popup.hide();
    }else{
    popup.show();
    }
  }
});

$(".messages_headers").on('click', function(){
  if ($('.messages_list').is(":visible")){
    $('.messages_list').hide();
  }else{
    $('.messages_list').show();
  }
});


    console.log("ready!");
    $(".edittweet").on("click", function () {
      $(".subscrire").show();
      window.scrollTo(0, 0);
      console.log("click");
    });

    $(".subscrire_button button").on("click", function () {
      $(".subscrire").hide();
    });
    $(".retweet").click(function () {
      var id = $(this).attr("id");
      var retweet = $(this).children("p").text();
      retweet = parseInt(retweet);
      console.log(retweet);
      $.ajax({
        url: "/retweet/" + id,
        type: "GET",
        success: function (data) { },
      });
      if ($(this).children("i").css("color") == "rgb(0, 128, 0)") {
        $(this).children("i").css("color", "white");
        $(this)
        .children("p")
        .text(retweet - 1);
      }else{
      $(this).children("i").css("color", "green");
      $(this)
        .children("p")
        .text(retweet + 1);
      }
    });
    $(".like").click(function () {
      var id = $(this).attr("id");
      var like = $(this).children("p").text();
      like = parseInt(like);
      $.ajax({
        url: "/like/" + id,
        type: "GET",
        success: function (data) { },
      });
      if ($(this).children("i").hasClass("bxs-heart")) {
        $(this).children("i").removeClass("bxs-heart");
        $(this).children("i").addClass("bx-heart");
        $(this).children("i").css("color", "white");
        $(this)
        .children("p")
        .text(like - 1);
      }else{
      $(this).children("i").removeClass("bx-heart");
      $(this).children("i").addClass("bxs-heart");
      $(this).children("i").css("color", "red");
      $(this)
        .children("p")
        .text(like + 1);
      }
    });
  

    $('#setLightMode').click(function(){
      $.ajax({
        url: "/setLightMode",
        type: "GET",
        success: function (data) { 
          window.location.reload();
        },
      });
    }
    );
    $('#setDarkMode').click(function(){
      $.ajax({
        url: "/setDarkMode",
        type: "GET",
        success: function (data) { 
          window.location.reload();
        },
      });
    }
    );
  });