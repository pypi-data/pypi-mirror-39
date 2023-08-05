
/*! qr-js v1.1.3 | (c) 2014 Alasdair Mercer | GPL v3 License
jsqrencode | (c) 2010 tz@execpc.com | GPL v3 License
// warning cf licence gpl3
// 
*/


app.angular.directive('qrcode', function ($timeout,$parse) {
    return {
        restrict: 'E',
        link: function (scope, element, attrs) {
			qr.image({
			    image: element.find('img')[0], //document.getElementById("qrcode"),
			    level: "Q",
			    size: 8,
			    value: 'exemple',
			  });


        },
        template: '<img alt="qrcode"></img>'
    }
});  

