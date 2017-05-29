/**
 * Created by Ivan Prymak on 3/31/2017.
 */
angular.module("shop", ['ngCookies'])
    .controller('ShopController', ['$scope', '$http', '$cookies', '$window',
        function ($scope, $http, $cookies, $window) {
            $scope.name = 'Shop';
            $scope.shop_items = [{'name': "Dummy", 'description': "Dummy description"}];
            $scope.filters = [{"name": "Filter", 'value': "", 'field': ""}];
            $scope.name_filter = function (index) {
                $scope.filters[index].name = "Name";
                $scope.filters[index].field = "name";
            };
            $scope.max_cost_filter = function (index) {
                $scope.filters[index].name = "Max cost";
                $scope.filters[index].field = "maxcost";
            };
            $scope.min_cost_filter = function (index) {
                $scope.filters[index].name = "Min cost";
                $scope.filters[index].field = "mincost";
            };
            $scope.packaging_filter = function (index) {
                $scope.filters[index].name = "Packaging";
                $scope.filters[index].field = "packaging";
            };
            $scope.designation_filter = function (index) {
                $scope.filters[index].name = "Designation";
                $scope.filters[index].field = "designation";
            };
            $scope.add_filter = function () {
                $scope.filters.push({"name": "Filter", 'value': "", 'field': ""});
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
            $http.get('/api/v1/manufacturers/').then(function (response) {
                $scope.manufacturers = response.data
            });
            $http.get('/api/v1/designations/').then(function (response) {
                $scope.designations = response.data
            });
            $scope.addToCart = function (id) {
                $http.post('/api/v1/cart/add/', {'id': id});
            };
            $scope.isCost = function (field) {
                return field === 'maxcost' || field === 'mincost';
            };
            $scope.styleCost = function (value) {
                var filler = '0';
                if (value % 100 > 9) {
                    filler = '';
                }
                return value / 100 + '.' + filler + value % 100;
            };
            $scope.$watchCollection('filters', function (newValue) {
                var validated_filters = newValue.filter(function (filter) {
                    return filter.field !== "" && filter.value !== "";
                });
                var req_params = _.object(_.pluck(validated_filters, 'field'), _.pluck(validated_filters, 'value'));
                $http({
                    url: "/api/v1/items/",
                    method: "GET",
                    params: req_params
                }).then(function (response) {
                    $scope.shop_items = response.data
                });
            });
            $scope.toCart = function () {
                $window.location.href = '/cart/';
            };
        }])
    .controller('CartController', ['$scope', '$http', '$cookies', '$window',
        function ($scope, $http, $cookies, $window) {
            $scope.cart_items = [{'name': "Dummy", 'description': "Dummy description"}];
            $http.get('/api/v1/cart/').then(function (response) {
                $scope.cart_items = response.data
            });
        }]);