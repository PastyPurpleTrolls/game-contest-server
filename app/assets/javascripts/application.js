// This is a manifest file that'll be compiled into application.js, which will include all the files
// listed below.
//
// Any JavaScript/Coffee file within this directory, lib/assets/javascripts, vendor/assets/javascripts,
// or vendor/assets/javascripts of plugins, if any, can be referenced here using a relative path.
//
// It's not advisable to add code directly here, but if you do, it'll appear at the bottom of the
// compiled file.
//
// Read Sprockets README (https://github.com/sstephenson/sprockets#sprockets-directives) for details
// about supported directives.
//
//= require jquery
//= require jquery_ujs
//= require turbolinks
//= require bootstrap
//= require_tree .

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

function redirectToContest() {
    var f = $("#contest-form")[0];
    var s = $("#contest-selector")[0];
    f.action = f.action.replace("contest_id", s.value);
    f.submit();
}

function removePlayer() {
    var selectedItem = $("#rightValues option:selected");
    $("#leftValues").append(selectedItem);
}

function addPlayer() {
    var selectedItem = $("#leftValues option:selected");
    $("#rightValues").append(selectedItem);
};

