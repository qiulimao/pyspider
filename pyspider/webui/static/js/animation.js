app.animation('.view-slide-in', function () {
 return {
 enter: function(element, done) {
  element.css({
  opacity: 0.3,
  position: "relative",
  top: "200px",
  left: "0px"
  })
  .animate({
  top: "0px",
  left: 0,
  opacity: 1
  }, 600, done);
 }
 };
}).animation('.repeat-animation', function () {
 return {
	 enter : function(element, done) {
	  var width = element.width();
	  element.css({
	  position: 'relative',
	  left: 200,
	  top:"0px",
	  opacity: 0.2
	  });
	  element.animate({
	  left: 0,
	  top:"0px",
	  opacity: 1,
	  }, 800,done);
	 },
 // leave : function(element, done) {
 //  element.css({
 //  position: 'relative',
 //  top: 0,
 //  left:"0px",
 //  opacity: 1
 //  });
 //  element.animate({
 //  top:0,
 //  left:-350,
 //  opacity: 0
 //  },1000, done);
 // },
 // move : function(element, done) {
 //  element.css({
 //  left: "20px",
 //  opacity: 0.2,
 //  });
 //  element.animate({
 //  left: "0px",
 //  opacity: 1
 //  }, done);
 // }
 };
});