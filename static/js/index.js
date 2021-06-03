$(document).ready(function () {
  $("#search").keydown(function(key){
    if(key.keyCode == 13){
      alert("error");
      window.location.replace('error.html');}
  });
});
