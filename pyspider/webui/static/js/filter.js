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
});