/**
 * Created by Ivan Prymak on 3/31/2017.
 */
angular.module('app')
    .controller('LoginController', ['$scope', '$http', '$cookieStore', '$window',
        function ($scope, $http, $cookieStore, $window) {
            $scope.name = 'Login';
            $scope.dismissAlert = function (alertName) {
                $scope[alertName] = false;
            };
            $scope.login = function (user) {
                $http.post('/api/v1/login/', user)
                    .then(function successCallback(response) {
                        $cookieStore.put('djangotoken', response.data['token']);
                        $window.location.href = '/';
                    }, function errorCallback(response) {
                        $scope.incorrectPair = true;
                    });
            };
        }])
    .controller('RegisterController', ['$scope', '$http', '$cookieStore', '$window',
        function ($scope, $http, $cookieStore, $window) {
            $scope.name = 'Register';
            $scope.dismissAlert = function (alertName) {
                $scope[alertName] = false;
            };
            $scope.register = function (user) {
                $scope.dataLoading = true;
                user.username = user.email;
                $http.post('/api/v1/register/', user)
                    .then(function successCallback(response) {
                        $window.location.href = '/';
                    }, function errorCallback(response) {
                        $scope.emailTaken = true;
                    });
            };
        }]);