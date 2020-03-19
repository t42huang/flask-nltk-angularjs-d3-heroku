(function () {
    'use strict';
  
    angular.module('TextAnalyzerApp', [])
  
    .controller('TextAnalyzerController', ['$scope', '$log', '$http', '$timeout',
      function($scope, $log, $http, $timeout) {
        $scope.getResults = function() {
          // $log.log("test");

          // get the url from the input
          const userInput = $scope.url;

          // fire the API request to start the task
          $http.post('/start', {"url": userInput})
            .success(function(jobId) {
                // $log.log(jobId); // log the job id
                getWordCountPoller(jobId);
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
                  } else if (status === 200){
                    $log.log(data); // log the word count result
                    $scope.wordcounts = data;
                    $timeout.cancel(timeout);
                    return false;
                  }
                  // continue to call the poller() function every 2 seconds
                  // until the timeout is cancelled
                  timeout = $timeout(poller, 2000);
                });
            };
            poller();
          }
      },
    ]);  
}());