app.
controller("IndexController",["$scope","$http","$interval","$timeout",function($scope,$http,$interval,$timeout){

	
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

	function auto_refresh_clock(){
		if ($scope.AUTO_REFRESH == true){
			$scope.refresh_countdown = $scope.refresh_countdown + 1;
			if ( $scope.refresh_countdown >= $scope.settings.AUTO_REFRESH_TIME){
				$scope.refresh_countdown = 0
			}			
		}
		else
		{
			$scope.refresh_countdown = 0;
		}

	}

	$scope.refresh_countdown = 0;

	$interval(auto_refresh_clock,1*1000);
	$timeout(function(){
		$scope.start_auto_refresh();
	},1*1000);

	$scope.projects = [];
	$scope.AUTO_REFRESH = false;
	$scope.STATUS = ['TODO','STOP','CHECKING','DEBUG','RUNNING'];
	$scope.refresh = refresh
	$scope.close_alert = close_alert;
	$scope.settings = {
		AUTO_REFRESH_TIME:3,
	}

	$scope.start_auto_refresh = function(){
		timing_refresh = $interval(refresh,$scope.settings.AUTO_REFRESH_TIME*1000);
		$scope.AUTO_REFRESH = true;
	}
	$scope.stop_auto_refresh = function(){
		if (timing_refresh){
			$interval.cancel(timing_refresh);
			$scope.AUTO_REFRESH = false;
		}
	}
	$scope.$watch('settings.AUTO_REFRESH_TIME',function(_new,_old,obj){
		$scope.stop_auto_refresh();
	});
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
	/*
     * 以下是测试：
	*/
}]).
controller("ResultController",["$scope","$routeParams","$resource","$location","$log","location","forecast",
	function($scope,$routeParams,$resource,$location,$log,location,forecast){
	
	$scope.project = $routeParams.project;
	$scope.refer = $routeParams.refer || "__self__";
	$scope.limit = $routeParams.limit || 10;
	$scope.current_page = $routeParams.page || 1;
	$scope.keylist = [];
	$scope.concentrate='';
	var result_resource = $resource('/result-list/:project/:refer/:limit/:page/',
		   {project:$scope.project,limit:$scope.limit,page:"@page",refer:"@refer"});
	

	function getpage(pagenum,refer){
		result_resource.get({page:pagenum,refer:refer}, function(response){
			$scope.num = response.count;
			$scope.results = response.results;
			$scope.project = response.project;
		});		
	}


	$scope.change_keylist = function (){
		$scope.keylist = forecast.predict($scope.results[0]["result"],$scope.concentrate);
	}


	$scope.page_turning = function(){

		getpage($scope.current_page,$scope.refer);
		url_indicator = "/result/"+$scope.project+"/"+$scope.refer+"/"+$scope.limit+"/"+$scope.current_page;
		location.skipReload().path(url_indicator).replace();		
	}

	$scope.refered = function(refer){
		var url_indicator;
		$scope.refer = refer;
		$scope.current_page = 1;
		getpage($scope.current_page,$scope.refer);
		url_indicator = "/result/"+$scope.project+"/"+refer+"/"+$scope.limit+"/"+"1";
		$location.path(url_indicator);
	}

	getpage($scope.current_page,$scope.refer);

}]).
controller("TaskController",["$scope","$routeParams","$resource",function($scope,$routeParams,$resource){
	$scope.hello="task";
	var project_name = $routeParams.project;
	var taskitems = $resource('/tasks/:project',{project:project_name})
	taskitems.get({},function(response){
		$scope.tasks = response.tasks;
	})

}]).
controller("DebugController",["$scope","$routeParams","$sce","$resource","$uibModal",
	function($scope,$routeParams,$sce,$resource,$uibModal){
	$scope.project = $routeParams.project;
	$scope.trust_url = $sce.trustAsResourceUrl("/debug/"+$routeParams.project);
	$scope.iframeHeiht = 750;
	$scope.heightup = function(){
		$scope.iframeHeiht += 5;
	}
	$scope.heightdown = function(){
        $scope.iframeHeiht -= 5;       
	}
	$scope.$watch("iframeHeiht",function(_new,_old,obj){
		if($scope.iframeHeiht > 1920 || $scope.iframeHeiht < 500){
			$scope.iframeHeiht = 750;
		} 		
	});
    
    var projectinfo = $resource('/debug/info/:project',{project:$scope.project});
    projectinfo.get({},function(response){
        $scope.projectinfo = response;
    });

    var dboperation = $resource("/debug/:operation/:db/:project",{operation:"clear",db:"@db",project:$scope.project});

	$scope.alert = function(db)
	{
        var deleteAlertModal = $uibModal.open({
              templateUrl: '/static/templates/delete-alert.html?v='+Math.random(),
              controller: 'DeleteDBAlertController',
              size: "sm",
              resolve: {
				project:function(){return $scope.project},
                targetdb: function () {
                  return db;
                },
              }
            });

        deleteAlertModal.result.then(function(response){
            if(response){
                dboperation.get({db:db},function(response){
					$scope.projectinfo = response;
				});
            }
        });		
	}


}]).
controller("DeleteDBAlertController",["$scope","$uibModalInstance","project","targetdb",
    function($scope,$uibModalInstance,project,targetdb){

          $scope.db = targetdb;
		  $scope.project = project;
          $scope.ok = function () {
            $uibModalInstance.close(true);
          };

          $scope.cancel = function () {
            $uibModalInstance.close(false);
          };
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
