/**
 * Created by milena on 04.04.17.
 */
var app = angular.module('app', ['authentication', 'shop'], function ($httpProvider, $interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
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
