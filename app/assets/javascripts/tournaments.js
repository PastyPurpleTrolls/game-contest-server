// Place all the behaviors and hooks related to the matching controller here.
// All this logic will automatically be available in application.js.
// You can use CoffeeScript in this file: http://coffeescript.org/
$(function () {
  var url = window.location.pathname;
  var id = url.substring(url.lastIndexOf('/') + 1);
  var data = $.getJSON("/brackets/" + id + ".json", function () {
  }).done(function (data) {
    // console.log(data);
    $('.bracket').bracket({
      init: data,
      teamWidth: 75,
      skipConsolationRound: true
    })
  });
});