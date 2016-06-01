app.factory('location', [
    '$location',
    '$route',
    '$rootScope',
    function ($location, $route, $rootScope) {
        $location.skipReload = function () {
            var lastRoute = $route.current;
            var un = $rootScope.$on('$locationChangeSuccess', function () {
                $route.current = lastRoute;
                un();
            });
            return $location;
        };
        return $location;
    }
]).factory('forecast', ['$filter', function($filter){
	return {
		predict:function(obj,on_typing_string){
			var obj = obj?obj:{};
			var last_obj;
			var _keys;
			var _parent_keys = [];
			var prefix = "";
			var possible_keys = [];

			if(/[a-zA-Z0-9_\.]+/.test(on_typing_string)){
				//正常匹配
				_keys = on_typing_string.split(".");
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
					possible_keys.push(prefix+"."+index);
				}
				else{
					possible_keys.push(index);
				}
				
			});
			return possible_keys;
		},
    }

}]);