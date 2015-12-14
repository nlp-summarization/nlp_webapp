(function () {

  'use strict';

  angular.module('NLPApp', [])
  .controller('NLPController', ['$scope', '$log', '$http', function($scope, $log, $http) {
  	$scope.$log = $log;
  	$scope.message = 'Hello World!';
  	$scope.summary = "Summary Not Generated";

// 		$scope.input_text = "Mr Peake and fellow crew members Yuri Malenchenko and Tim Kopra floated through the hatch from their Soyuz space capsule to be greeted by the resident ISS astronauts. \
// The three new passengers arrived at the space platform following a six-hour journey after launch from Kazakhstan. \
// Earlier, the Russian commander had to steer the craft to dock with the ISS. \
// It followed complications with the usual automatic docking procedure. \
// It's a rare event for the Soyuz crew to have to manually dock the spacecraft at the space station. \
// The Kurs radar system that failed is one of the two main ways controllers have of determining where the Soyuz is relative to the space station. \
// The other is measurements taken from the ground. \
// The immense skill required to manually dock the capsule in open space is exactly why Tim and the other crew members undergo such rigorous training for a range of different failure scenarios."

  	$scope.input_text =  "Triceratops, one of the most widely recognizable of the dinosaurs that once roamed our planet, has a new cousin. \
Known for its three-horned head and bony, frilly collar, the triceratops somewhat resembles the modern-day rhinoceros. \
But not only is its new relative older -- by 100 million years -- it also looks dramatically different. \
Discovered in the Gobi Desert in northwestern China, hualianceratops 'provides significant information on the early evolution of horned dinosaurs,' says paleontologist Xu Xing, who worked on the discovery announced Wednesday.";
  	
  	$scope.data = {
	    repeatSelect: 1,
	    availableOptions: [
	      {id: '1', name: 'Baseline'},
	      {id: '2', name: 'Page Rank'},
	      {id: '3', name: 'LSA'},
	      {id: '4', name: 'Lex Rank'}
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