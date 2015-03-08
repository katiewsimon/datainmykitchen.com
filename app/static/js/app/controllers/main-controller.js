app.controller('MainController', ['$scope', '$http',
    function MainController($scope, $http) {

        $scope.foodItems = {};
        $scope.foodItems.data = [];

        $scope.nutrients = {};
        $scope.nutrients.data = [];

		$scope.addFood = function(foodItem) {
	        $scope.foodItems.data.push({
	            id: $scope.foodItems.data.length + 1,
	            foodItem: foodItem
	        });
	    }

	    $scope.updateRecommendation = function(){
	    	var foodList = $scope.foodItems.data;
	    	var ids = "";
	    	for (var i = 0; i < foodList.length; i++){
	    		ids += foodList[i].foodItem.NDB_No;
				ids += ","
	    	}
	    	ids = ids.substring(0, ids.length - 1);

	    	$http.get('/recommendation?foods=' + ids).success(function(response){
	    		console.log(response.nutrients);
	    		$scope.nutrients.data = response.nutrients;
	    	});
	    }

        $scope.$watch('selectedFood', function(newValue, oldValue){
        	if (null == newValue){
        		return;
        	}

        	$scope.addFood(newValue.originalObject);

        	$scope.updateRecommendation();
        });
    }
]);
