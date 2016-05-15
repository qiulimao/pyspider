var app = angular.module('pyspider', ['ui.bootstrap','ngRoute']);

app.config(["$interpolateProvider","$routeProvider",function($interpolateProvider,$routeProvider) {
  $interpolateProvider.startSymbol('[$');
  $interpolateProvider.endSymbol('$]');

  $routeProvider
  			.when('/', {
                controller: 'IndexController',
                templateUrl: 'static/templates/index.html'
            })
  			.when('/task', {
                controller: 'TaskController',
                templateUrl: 'static/templates/tasks.html'
            })   
  			.when('/result', {
                controller: 'ResultController',
                templateUrl: 'static/templates/results.html'
            })                      
            .otherwise({
                redirectTo: '/'
            });

}]);