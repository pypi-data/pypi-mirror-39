

app.angular.directive('barchart', function ($parse) {
    return {
        restrict: 'E',
        link: function (scope, element, attrs) {

            var data = [10,20,30,40,60];
            //in D3, any selection[0] contains the group
            //selection[0][0] is the DOM node
            //but we won't need that this time
            var chart = d3.select(element[0]);
            //to our original directive markup bars-chart
            //we add a div with out chart stling and bind each
            //data entry to the chart
            chart.append("div").attr("class", "chart")
                .selectAll('div')
                .data(data).enter().append("div")
                .transition().ease("elastic")
                .style("width", function(d) { return d + "%"; })
                .text(function(d) { return d + "%"; });
            //a little of magic: setting it's width based
            //on the data value (d) 
            //and text all with a smooth transition

        }
    }
});  


app.angular.directive('piechart', function($timeout) {
    return {
        restrict: 'E',
        scope: true,
        controller: ['$scope','$element','$q',function ($scope,$element,$q) {   
            this.svg = $element.find('svg')[0]
            this.data = [
                  {
                    "label": "One",
                    "value" : 29.765957771107
                  } ,
                  {
                    "label": "Two",
                    "value" : 0
                  } ,
                  {
                    "label": "Three",
                    "value" : 32.807804682612
                  } ,
                  {
                    "label": "Four",
                    "value" : 196.45946739256
                  } ,
                  {
                    "label": "Five",
                    "value" : 0.19434030906893
                  } ,
                  {
                    "label": "Six",
                    "value" : 98.079782601442
                  } ,
                  {
                    "label": "Seven",
                    "value" : 13.925743130903
                  } ,
                  {
                    "label": "Eight",
                    "value" : 5.1387322875705
                  }
            ]
            var self = this
            this.build = function() {
                nv.addGraph(function() {

                  var chart = nv.models.pieChart()
                      .x(function(d) { return d.label })
                      .y(function(d) { return d.value })
                      .showLabels(true);

                    
                    d3.select(self.svg)
                        .datum(self.data)
                        .transition().duration(1200)
                        .call(chart);

                  return chart;
                });
            }
        }],
        link: function(scope, element, attrs, ctrl,transclude) {
            $timeout(function() {
                ctrl.build()
            });
        },
        controllerAs: 'd3',
        template:  `
            <style>
            svg {
              width: 300px;  
              height: 200px;
              border: solid 1px #000
            }
            </style>

            <div >
              <svg></svg>
            </div>
        `
    }
});  
