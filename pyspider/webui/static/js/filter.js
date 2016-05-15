app.filter("spidergroup", function() {
    var spidergroup = function(group) {
    	if (! group){
    		return "[group]"
    	}
    	return group
    };
    
    return spidergroup;
});