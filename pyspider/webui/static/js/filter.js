app.filter("null2group", function() {
    var null2group = function(group) {
    	if (! group){
    		return "[group]"
    	}
    	return group
    };
    
    return null2group;

}).filter("null2zero",function(){
	var null2zero = function(number){
		if (! number){
			return 0;
		}
		else {
			return number;
		}
	}
	return null2zero;
}).filter("null2one",function(){
    return function(number){
        if (number==0){
            return 1;
        }
        return number;
    }

}).filter('asHTML',["$sce","$filter",function($sce,$filter) {
  return function(input) {
  	if(typeof input=='string'){
        return $sce.trustAsHtml(input)
    }
    else if(angular.isObject(input)){
        return "<pre>"+$filter('json')(input)+"</pre>";
    }
    //var data  = $sce.trustAs($sce.HTML, input);
    //data = $.trustAs($sce.URL,data);
    return input;
  };
}]).filter("asURL",["$sce",function($sec){
	return function(input){
        if(typeof input == 'string'){
            return $sec.trustAs($sec.URL,input);
        }
		return input
	}
}]).filter("refreshCounter",function(){
    return function(input,count){
        if(input == 0){
            return 0
        }
        
        return count - input
    }
}).filter("spotlight",["$log",function($log){
    function __str__(result){
        if(angular.isObject(result)){
            return "<Object>";
        }
        if(angular.isString(result)){
            r = result.length<18?result:result.slice(0,18)+"...";
            return r;
        }
        else{
            return result;
        }
    }

    return function(obj,key){
        var _keys;
        var result = obj;
        if(!key){
            return "";
        }
        if (!/[a-zA-Z0-9_\.]+/.test(key)){
            return "InvalidKey";
        }
        _keys = key.split(".");

        try{
           for(i in _keys){
              result = result[_keys[i]];
              if (result == undefined){
                return "Invalidkey";
              }
           }
           return __str__(result);
        }
        catch(err){
            return "NotFound";
        }

    }
}]).filter("partfilter",["$filter",function($filter){
    return function(input,value){
        var part_key;
        part_key = value.split(".").pop();
        return $filter("filter")(input,part_key);
    }
}]).filter("templateinclude",["$filter",function($filter){
    return function(template_name)
    {
        var template_name = template_name +"?v="+Math.floor(Math.random()*10000+99);
        return template_name;
    }
}]);