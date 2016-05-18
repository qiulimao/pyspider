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
}).filter('asHtml',["$sce",function($sce) {
  return function(input) {
  	if(typeof input=='string'){
        return $sce.trustAsHtml(input)
    }
    //var data  = $sce.trustAs($sce.HTML, input);
    //data = $.trustAs($sce.URL,data);
    //return data;
  };
}]).filter("asULR",["$sce",function($sec){
	return function(input){
		return $sec.trustAs($sec.URL,input);
	}
}]);