
function map(target) {

    var mymap = window.map = L.map('mymap').setView([51.505, -0.09], 7);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
	        '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
	        'Imagery © <a href="http://mapbox.com">Mapbox</a>',
        id: 'mapbox.streets'
    }).addTo(mymap);

    var lat = 51.000 //data['latitude']
    var long = -0.09 //data['longitude']
    var info = 'description' //data['description']
    var marker = L.marker([lat,long]).addTo(mymap);
    marker.bindPopup(info).openPopup();  

    /*
    $.ajax('data/geo.json').then(function(data) {
        
        $(data).each( function(index,val ) {
            var marker = L.marker([val['lat'],val['long']]).addTo(mymap);
            var info = val['name']+'\n'+val['address']
            marker.bindPopup(info).openPopup(); 
        })
    })
    */
    return mymap
}




app.angular.directive('map', function($timeout) {
    return {
        restrict: 'E',
        scope: true,
        controller: ['$scope','$element','$q',function ($scope,$element,$q) {   
        	this.map = null
            this.init = function() {
            	this.map = map()
            }
        }],
        link: function(scope, element, attrs, ctrl,transclude) {
			$timeout(function() {
			    ctrl.init()
			});
        },
        controllerAs: 'map',
        template: '<div id="mymap" style="width:400px; height:400px; border: solid 1px #000">geo map</div>',
    }
});  


