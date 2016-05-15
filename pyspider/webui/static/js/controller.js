app.
controller("IndexController",["$scope","$http",function($scope,$http){
	$scope.hello="qiulimao";
	$scope.STATUS = ['TODO','STOP','CHECKING','DEBUG','RUNNING'];

	function refresh_projects(){
		$http.get("/projects-list").success(function(response){
			$scope.projects = response.projects
		});		
	};

  $scope.dynamicPopover = {
    content: 'Hello, World!',
    changeStatustemplateUrl: 'changeStatusTemplate.html',
    title: 'Title'
  };

	$scope.refresh_projects = refresh_projects

	function init(){
		refresh_projects();
	}
	init();
}]).
controller("ResultController",["$scope",function($scope){
	$scope.hello="result";
}]).
controller("TaskController",["$scope",function($scope){
	$scope.hello="task";
}]);