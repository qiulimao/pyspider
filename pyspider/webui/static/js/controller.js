app.
controller("IndexController",["$scope","$http","$interval",function($scope,$http,$interval){

	
	var timing_refresh;

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

	function monitor(){
		/*  
			{"mala":{"all": {"success": 133}}, 
			"www_wooyun_org": { "1d": {"pending": 118, "retry": 10, "success": 113}, 
								"1h": {"pending": 118, "retry": 10, "success": 113}, 
								"all": {"pending": 5, "success": 111}
								}
			}
		*/
		$http.get("/counter").success(function(response){
			angular.forEach($scope.projects,function(data,index,defaultarray){
				//遍历projects,让他们用project去找各自状态
				if($scope.projects[index]){
					$scope.projects[index].monitor = response[data.name];
				}
			});
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

	function refresh(){
		refresh_queues();
		refresh_projects();
		monitor();
	}

	function init(){
		refresh();
	}

	$scope.projects = [];
	$scope.AUTO_REFRESH = false;
	$scope.STATUS = ['TODO','STOP','CHECKING','DEBUG','RUNNING'];
	$scope.refresh = refresh
	$scope.close_alert = close_alert;

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



	init();
}]).
controller("ResultController",["$scope","$routeParams","$resource",function($scope,$routeParams,$resource){
	$scope.hello=$routeParams.project;
	var ITERM_PER_PAGE = 10;
	var ProjectItems = $resource('/result-list/:project/:itemPerPage/:page/', {project:$routeParams.project,itemPerPage:ITERM_PER_PAGE,page:"@page"});
	$scope.CurrentPage = 1;

	function getpage(pagenum){
		ProjectItems.get({page:pagenum}, function(response){
			$scope.num = response.count;
			$scope.results = response.results;
			$scope.project = response.project;
		});		
	}
	getpage(1);

	$scope.$watch('CurrentPage',function(new_value,old_value,_scope){
		if(new_value){
			getpage(new_value);
		}
		
	})

}]).
controller("TaskController",["$scope","$routeParams",function($scope,$routeParams){
	$scope.hello="task";
}]).
controller("DebugController",["$scope","$routeParams","$sce",function($scope,$routeParams,$sce){
	$scope.project = $routeParams.project;
	$scope.trust_url = $sce.trustAsResourceUrl("/debug/"+$routeParams.project);
}]).
controller('CreateNewSpider', ['$scope',"$http","$location","$log", function($scope,$http,$location,$log){
	$scope.newproject={}

	$scope.create_new_spider = function(){

  		var new_project_info = {
  			"project-name":$scope.newproject.project_name,
  			"start-urls":$scope.newproject.start_url,
  			"script-mode":"script"
  		}

		$http({
	        method  : 'POST',
	        url     : '/debug/create-project',
	        data    : $.param(new_project_info), 
	        headers : { 'Content-Type': 'application/x-www-form-urlencoded' }  
		}).success(function(response){
			var project_name = response.project_name;
			var next_url = "/debug/"+project_name;
			$location.path(next_url);
		});
	}

}]);