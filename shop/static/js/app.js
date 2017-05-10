/**
 * Created by milena on 04.04.17.
 */
angular.module('app', ['authentication', 'shop'], function ($httpProvider, $interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});