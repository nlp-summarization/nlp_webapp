(function () {

  'use strict';

  angular.module('NLPApp', [])
  .controller('NLPController', ['$scope', '$log', '$http', function($scope, $log, $http) {
  	$scope.$log = $log;
  	$scope.message = 'Hello World!';
  	$scope.summary = "Summary Not Generated";
  	$scope.input_text = "this is a sample input text";

  	$scope.data = {
	    repeatSelect: 1,
	    availableOptions: [
	      {id: '1', name: 'Naive Bayes'},
	      {id: '2', name: 'Page Rank'},
	      {id: '3', name: 'LSA'}
	    ],
	   };

    $scope.getResults = function() {
      $log.log("test");
      $log.log($scope.data.repeatSelect);

      $http.post('/summary/:id', {"id": $scope.data.repeatSelect}).
	    success(function(results) {
	      $log.log(results);
	      $scope.summary = results["summary"];
	    }).
	    error(function(error) {
	      $log.log(error);
	    });

    };
  }

  ]);

}());