/**
 * Created by milena on 04.04.17.
 */
var app = angular.module('app', ['ngCookies', 'ngRoute'], function ($httpProvider, $interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

}).run(function ($cookieStore, $rootScope, $http) {
    if ($cookieStore.get('djangotoken')) {
        $http.defaults.headers.common['Authorization'] = 'Token ' + $cookieStore.get('djangotoken');
    }
});
app.config(['$routeProvider', '$locationProvider',
    function ($routeProvider, $locationProvider) {
        var onlyLoggedIn = function ($location, $cookieStore, $q) {
            var deferred = $q.defer();
            if ($cookieStore.get('djangotoken')) {
                deferred.resolve();
            } else {
                deferred.reject();
                $location.url('/login');
            }
            return deferred.promise;
        };
        $routeProvider.when('/', {
            templateUrl: 'static/html/shop.html',
            controller: 'ShopController',
            resolve: {loggedIn: onlyLoggedIn}
        }).when('/login', {
            templateUrl: 'static/html/login.html',
            controller: 'LoginController'
        }).when('/register', {
            templateUrl: 'static/html/register.html',
            controller: 'RegisterController'
        }).when('/cart', {
            templateUrl: 'static/html/cart.html',
            controller: 'CartController',
            resolve: {loggedIn: onlyLoggedIn}
        }).otherwise({
            redirectTo: '/login'
        });
        $locationProvider.html5Mode(true);
    }]);

app.directive('costField', function ($parse) {
    return {
        restrict: 'A',
        scope: {
            'costField': '&'
        },
        link: function (scope, element, attr) {
            var x = $parse(attr.costField);
            var result = x(scope, {});
            scope.$watch('costField()', function (newValue) {
                if (newValue)
                    $(element).numeric({decimal: ".", decimalPlaces: 2, negative: false},
                        function () {
                            this.value = "";
                            this.addClass("error");
                            this.focus();
                        });
            });
        }
    }
});
app.directive('materialTextInput', function () {
    return {
        restrict: 'C',
        transclude: true,
        link: function (scope, el) {
            el.find('input')
                .focus(function () {
                    el.addClass('material-text-input-focused');
                })
                .blur(function () {
                    el.removeClass('material-text-input-focused');
                });
        },
        template: '<ng-transclude></ng-transclude>'

    };
});
