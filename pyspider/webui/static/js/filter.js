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

}).filter('asHTML',["$sce",function($sce) {
  return function(input) {
  	if(typeof input=='string'){
        return $sce.trustAsHtml(input)
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
});