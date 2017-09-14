function HomeCtrl($http) {
    var ctrl = this;
    this.getGreeting = function (name) {
        $http.post('/greeting', {name: name})
            .success(function (response) {
                         ctrl.greeting = response.greeting;
                     });
    }
}

angular.module('app', [])
    .controller('HomeCtrl', HomeCtrl);