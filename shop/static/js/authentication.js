/**
 * Created by Ivan Prymak on 3/31/2017.
 */
angular.module("authentication", [], function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]')
})

    .controller('LoginController', LoginController)
    .controller('RegisterController', RegisterController);

function LoginController($scope) {
    $scope.name = 'Login';
}
LoginController.$inject = ['$scope'];

function RegisterController($scope) {
    $scope.name = 'Register';
}
RegisterController.$inject = ['$scope'];