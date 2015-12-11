(function () {

  'use strict';

  angular.module('NLPApp', [])
  .controller('NLPController', ['$scope', '$log', '$http', function($scope, $log, $http) {
  	$scope.$log = $log;
  	$scope.message = 'Hello World!';
  	$scope.summary = "Summary Not Generated";
  	$scope.input_text =  "Thomas A. Anderson is a man living two lives. By day he is an \
average computer programmer and by night a hacker known as \
Neo. Neo has always questioned his reality, but the truth is \
far beyond his imagination. Neo finds himself targeted by the \
police when he is contacted by Morpheus, a legendary computer \
hacker branded a terrorist by the government. Morpheus awakens \
Neo to the real world, a ravaged wasteland where most of \
humanity have been captured by a race of machines that live \
off of the humans' body heat and electrochemical energy and \
who imprison their minds within an artificial reality known as \
the Matrix. As a rebel against the machines, Neo must return to \
the Matrix and confront the agents: super-powerful computer \
programs devoted to snuffing out Neo and the entire human \
rebellion.";
  	
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

      $http({
	      url: "/summary/",
	      method: "POST",
	      headers: { 'Content-Type': 'application/json' },
	      data: {"id": $scope.data.repeatSelect, "raw_text": $scope.input_text}
	    }).success(function(data) {
	      console.log(data)
	      $scope.summary = data["summary"];
	    }).
	    error(function(error) {
	      $log.log(error);
	    });

     //  $http.post('/summary', {"id": $scope.data.repeatSelect, "raw_text": $scope.input_text}).
	    // success(function(results) {
	    //   $log.log(results);
	    //   $scope.summary = results["summary"];
	    // }).
	    // error(function(error) {
	    //   $log.log(error);
	    // });

    };
  }

  ]);

}());