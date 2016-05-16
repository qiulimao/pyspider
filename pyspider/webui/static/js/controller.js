app.
controller("IndexController",["$scope","$http","$interval",function($scope,$http,$interval){
	$scope.hello="qiulimao";
	$scope.STATUS = ['TODO','STOP','CHECKING','DEBUG','RUNNING'];

	function refresh_projects(){
		$http.get("/projects-list").success(function(response){
			$scope.projects = response.projects
		});
		refresh_queues();
	};
	function refresh_queues(){
		$http.get("/queues").success(function(response){
			$scope.queues = response;
			/*
			fetcher2processor newtask_queue
			processor2result scheduler2fetcher status_queue
			*/
		});
	}
	function refresh(){
		refresh_queues();
		refresh_projects();
	}

	var timing_refresh;
	$scope.refresh = refresh
	$scope.AUTO_REFRESH = false;
	$scope.start_auto_refresh = function(){
		timing_refresh = $interval(refresh,8*1000);
		$scope.AUTO_REFRESH = true;
	}
	$scope.stop_auto_refresh = function(){
		if (timing_refresh){
			$interval.cancel(timing_refresh);
			$scope.AUTO_REFRESH = false;
		}
	}

	function init(){
		refresh();
	}
	$scope.update = function(pk,name,value){
		var postdata = {
			'pk':pk,
			"name":name,
			"value":value
		}
		$http({
        method  : 'POST',
        url     : '/update',
        data    : $.param(postdata), 
        // pass in data as strings
        headers : { 'Content-Type': 'application/x-www-form-urlencoded' }  
        // set the headers so angular passing info as form data (not request payload)
    	}).success(function(response){

    	});
	}

	function show_alert(project_name,project_status){
		$scope.SHOW_ALERT = true;
		$scope.alert = {
			"msg":"only project in RUNNING and DEBUG can run....",
			"status":project_status
		}
	}
	function close_alert(){
		$scope.SHOW_ALERT = false;
	}

	$scope.close_alert = close_alert;

	$scope.run = function(project){
		var RUNNABLE_STATUS = ["RUNNING","DEBUG"];
		if (project.status == "RUNNING" || project.status == "DEBUG"){
			close_alert();

			$http({
		        method  : 'POST',
		        url     : '/run',
		        data    : $.param({"project":project.name}), 
		        headers : { 'Content-Type': 'application/x-www-form-urlencoded' }  
			}).success(function(response){
				// response.result
			});
		}
		else{
			show_alert(project.name,project.status);
		}
	}

	$scope.runing_monitor = function(project){
		/*  
			{"mala":{"all": {"success": 133}}, 
			"www_wooyun_org": { "1d": {"pending": 118, "retry": 10, "success": 113}, 
								"1h": {"pending": 118, "retry": 10, "success": 113}, 
								"all": {"pending": 5, "success": 111}
								}
			}
		*/
	}

	init();
}]).
controller("ResultController",["$scope",function($scope){
	$scope.hello="result";
}]).
controller("TaskController",["$scope",function($scope){
	$scope.hello="task";
}]);