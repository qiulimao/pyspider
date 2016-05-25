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
controller("ResultController",["$scope","$routeParams","$resource","$location","$log",function($scope,$routeParams,$resource,$location,$log){
	
	//var $scope.limit = $routeParams.limit || 10;
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
	getpage($scope.current_page,$scope.refer);

	$scope.change_keylist = function (){
		var obj = $scope.results?$scope.results[0]["result"]:{};
		var last_obj;
		var _keys;
		var _parent_keys = [];
		var prefix = "";
		$scope.keylist = [];

		if(/[a-zA-Z0-9_\.]+/.test($scope.concentrate)){
			//正常匹配
			_keys = $scope.concentrate.split(".");
			for(i in _keys){
				last_obj = obj;
				obj = obj[_keys[i]];
				if (obj==undefined){
					obj = last_obj;
					break;
				}
				if(!angular.isObject(obj)){
					obj = last_obj;
					break;
				}
				_parent_keys.push(_keys[i]);
			}
		}
		
		prefix = _parent_keys.join(".");
		angular.forEach(obj,function(data,index,array){
			if(prefix){
				$scope.keylist.push(prefix+"."+index);
			}
			else{
				$scope.keylist.push(index);
			}
			
		});

	}

	$scope.$watch('current_page',function(new_value,old_value,_scope){

		if(new_value == old_value){
			return 
		}
		url_indicator = "/result/"+$scope.project+"/"+$scope.refer+"/"+$scope.limit+"/"+new_value;
		$location.path(url_indicator);
		//$location.hash("result");
		
	});
	$scope.refered = function(refer){
		var url_indicator;
		$scope.refer = refer;
		$scope.current_page = 1;
		url_indicator = "/result/"+$scope.project+"/"+refer+"/"+$scope.limit+"/"+"1";
		$location.path(url_indicator);
	}

}]).
controller("TaskController",["$scope","$routeParams","$resource",function($scope,$routeParams,$resource){
	$scope.hello="task";
	var project_name = $routeParams.project;
	var taskitems = $resource('/tasks/:project',{project:project_name})
	taskitems.get({},function(response){
		$scope.tasks = response.tasks;
	})

}]).
controller("DebugController",["$scope","$routeParams","$sce",function($scope,$routeParams,$sce){
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