(function () {
    'use strict';
  
    angular.module('TextAnalyzerApp', [])
  
    .controller('TextAnalyzerController', ['$scope', '$log', '$http', '$timeout',
      function($scope, $log, $http, $timeout) {
        $scope.submitButtonText = 'Submit';
        $scope.loading = false;
        $scope.urlerror = false;

        $scope.getResults = function() {
          // $log.log("test");

          // get the url from the input
          const userInput = $scope.url;

          // fire the API request to start the task
          $http.post('/start', {"url": userInput})
            .success(function(jobId) {
                // $log.log(jobId); // log the job id
                getWordCountPoller(jobId);

                $scope.wordcounts = null; // clear out old result
                $scope.loading = true; // disable submit button
                $scope.submitButtonText = "Loading"; // change submit button text
            })
            .error(function(error) {
                $log.log(error);
            })
        };

        function getWordCountPoller(jobID) { // poller checks every 2 sec
            var timeout = "";
          
            var poller = function() {
              // fire another request
              $http.get('/results/'+jobID)
                .success(function(data, status, headers, config) {
                  if (status === 202) {
                    $log.log(data, status); // log job status: work in progress
                  } else if (status === 200) {
                    $log.log(data); // log the word count result
                    
                    $scope.urlerror = false;
                    $scope.loading = false;
                    $scope.submitButtonText = "Submit";
                    $scope.wordcounts = data;

                    $timeout.cancel(timeout);
                    return false;
                  }
                  // continue to call the poller() function every 2 seconds
                  // until the timeout is cancelled
                  timeout = $timeout(poller, 2000);
                })
                .error(function(error) {
                    $log.log(error);
                    $scope.loading = false;
                    $scope.submitButtonText = "Submit";
                    $scope.urlerror = true;
                });
            };
            poller();
          }
      },
    ])

    .directive('wordCountChart', ['$parse', function ($parse) {
        return {
          restrict: 'E',
          replace: true,
          template: '<div id="chart"></div>',
          link: function (scope) {
            scope.$watch('wordcounts', function() {
              d3.select('#chart').selectAll('*').remove();
              var data = scope.wordcounts;
              for (var word in data) {
                var key = data[word][0];
                var value = data[word][1];
                d3.select('#chart')
                  .append('div')
                  .selectAll('div')
                  .data(word)
                  .enter()
                  .append('div')
                  .style('width', function() {
                    return (value * 3) + 'px';
                  })
                  .text(function(d){
                    return key;
                  });
              }
            }, true);
          }
         };
      }]);
}());