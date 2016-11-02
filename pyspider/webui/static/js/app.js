var app = angular.module('weblocust', ['ui.bootstrap','ngRoute','ngResource','ngSanitize','ngAnimate']);

app.config(["$interpolateProvider",
            "$routeProvider",
            "$sceDelegateProvider",
function($interpolateProvider,$routeProvider,$sceDelegateProvider) {
  $interpolateProvider.startSymbol('[$');
  $interpolateProvider.endSymbol('$]');

  $routeProvider
  			.when('/', {
                controller: 'IndexController',
                templateUrl: 'static/templates/index.html'
            })
  			.when('/task/:project', {
                controller: 'TaskController',
                templateUrl: 'static/templates/tasks.html'
            })
        .when('/debug/:project', {
                controller: 'DebugController',
                templateUrl: 'static/templates/debug.html'
            })               
  			.when('/result/:project', {
                controller: 'ResultController',
                templateUrl: 'static/templates/results.html'
            })  
        .when('/result/:project/:refer/:limit/:page', {
                controller: 'ResultController',
                templateUrl: 'static/templates/results.html'
            })                               
        .otherwise({
                redirectTo: '/'
            });

  $sceDelegateProvider.resourceUrlWhitelist([
        'self',
        '**'
        ]);


}]);