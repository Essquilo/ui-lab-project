/**
 * Created by Ivan Prymak on 3/31/2017.
 */
angular.module("shop", ['ngCookies'])
    .controller('ShopController', ['$scope', '$http', '$cookies', '$window',
        function ($scope, $http, $cookies, $window) {
            $scope.name = 'Shop';
            $scope.shop_items = [{'name': "Dummy", 'description': "Dummy description"}];
            $scope.filters = [{'field': "Filter", 'value': ""}];
            $scope.name_filter = function (index) {
                $scope.filters[index].field = "Name";
            };
            $scope.max_cost_filter = function (index) {
                $scope.filters[index].field = "Max cost";
            };
            $scope.min_cost_filter = function (index) {
                $scope.filters[index].field = "Min cost";
            };
            $scope.packaging_filter = function (index) {
                $scope.filters[index].field = "Packaging";
            };
            $scope.designation_filter = function (index) {
                $scope.filters[index].field = "Designation";
            };
            $scope.add_filter = function () {
                $scope.filters.push({'field': "Filter", 'value': ""});
            };
            $scope.remove_filter = function (index) {
                $scope.filters.splice(index, 1);
            };
            $http.get('/api/v1/items/').then(function (response) {
                $scope.shop_items = response.data
            });
            $http.get('/api/v1/packaging/').then(function (response) {
                $scope.packagings = response.data
            });
            $http.get('/api/v1/manufacturer/').then(function (response) {
                $scope.manufacturers = response.data
            });
            $http.get('/api/v1/designation/').then(function (response) {
                $scope.designations = response.data
            });
            $scope.addToCart = function (id) {
                var cart = $cookies.get('cart');
                if (!cart)
                    cart = [];
                cart.add(id);
                $cookies.put('cart', cart);
            };
        }]);