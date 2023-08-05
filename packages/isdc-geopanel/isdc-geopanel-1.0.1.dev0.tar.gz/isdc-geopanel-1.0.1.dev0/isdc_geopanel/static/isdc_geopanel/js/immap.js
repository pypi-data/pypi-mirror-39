$(function () {
  var pathArray = window.location.pathname.split('/');
  var segment_3 = pathArray[3];
  var segment_2 = pathArray[2];
  
  if (segment_3 == 'view') {
    var getSet = htmlDecode(PACKAGE);
    var arrSet = getSet.replace(/'/g, '"');
    var isdcPackage = JSON.parse(arrSet);
    
    addDiv(isdcPackage);
    console.log(isdcPackage);
  }

})

function htmlDecode(value) {
  return $("<textarea/>").html(value).text();
}

function addDiv(isdcPackage) {
  var getId = document.getElementById('mapleftbox');
  var div = document.createElement('div');
  div.setAttribute('id', 'isdcpanel');
  getId.appendChild(div);

  $.getScript(STATIC_URL + "isdc_geopanel/js/immap.panel.js", function(){
    var config = isdcPackage[0].panel_setting;
    var package = isdcPackage[1].official_package;
    var options = {panelConfig: config, addPackage: package};
    var addPanel = new window.Panel('isdcpanel', options);
    addPanel.panel();
  }, 100);
}
