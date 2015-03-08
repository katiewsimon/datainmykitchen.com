app.controller('MainController', ['$scope', '$http',
    function MainController($scope, $http) {

        $scope.foodItems = {};
        $scope.foodItems.data = [];

		$scope.addFood = function (foodItem) {
	        $scope.foodItems.data.push({
	            id: $scope.foodItems.data.length + 1,
	            foodItem: foodItem
	        });
	    }

        $scope.$watch('selectedFood', function(newValue, oldValue){
        	if (null == newValue){
        		return;
        	}

        	$scope.addFood(newValue.originalObject);
        });
    }
]);
