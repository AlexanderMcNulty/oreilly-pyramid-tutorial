function TitleService() {
    this.siteName = 'MySite';
    this.title = '';
    this.setPageTitle = function (pageTitle) {
        this.title = pageTitle + ' - ' + this.siteName;
    };
    this.setPageTitle('Home');
}

function ToDoFactory($resource) {
    return $resource('/api/todos/:id', {id: '@id'},
        {
            update: {
                method: 'PUT' // this method issues a PUT request
            }
        });
}

function SiteCtrl(TitleService) {
    this.TitleService = TitleService;
}

function HomeCtrl(TitleService) {
    TitleService.setPageTitle('Home');
}

function ToDosCtrl(ToDo, TitleService) {
    var ctrl = this;
    TitleService.setPageTitle('ToDos');
    this.todos = ToDo.query();
    this.delete = function (todo) {
        todo.$delete(
            function () {
                // Refresh list after deleting
                ctrl.todos = ToDo.query();
            }
        )
    }
}

function ToDosAddCtrl($location, TitleService, ToDo) {
    TitleService.setPageTitle('Add ToDo');
    this.create = function (newTitle) {
        var todo = new ToDo({title: newTitle});
        todo.$save(function (response) {
            var newId = response.id.toString();
            $location.path('/todos/' + newId);
        });
    }
}

function ToDosViewCtrl($routeParams, TitleService, ToDo) {
    TitleService.setPageTitle('View ToDo');
    var id = $routeParams.id;
    this.todo = ToDo.get({id: id});
}

function ToDosEditCtrl($location, $routeParams, TitleService, ToDo) {
    TitleService.setPageTitle('Edit ToDo');
    var id = $routeParams.id;
    this.todo = ToDo.get({id: id});
    this.update = function () {
        this.todo.$update(
            function (response) {
                $location.path('/todos/' + id);
            }
        );
    }
}

function ModuleConfig($routeProvider) {

    $routeProvider.
        when('/', {
            templateUrl: 'home.html',
            controller: 'HomeCtrl as ctrl'
        }).
        when('/todos/add', {
            templateUrl: 'todos_add.html',
            controller: 'ToDosAddCtrl as ctrl'
        }).
        when('/todos/:id', {
            templateUrl: 'todos_view.html',
            controller: 'ToDosViewCtrl as ctrl'
        }).
        when('/todos/:id/edit', {
            templateUrl: 'todos_edit.html',
            controller: 'ToDosEditCtrl as ctrl'
        }).
        when('/todos', {
            templateUrl: 'todos_list.html',
            controller: 'ToDosCtrl as ctrl'
        }).
        otherwise({
            redirectTo: '/'
        });
}

angular.module('app', ['ngResource', 'ngRoute'])
    .factory('ToDo', ToDoFactory)
    .service('TitleService', TitleService)
    .controller('SiteCtrl', SiteCtrl)
    .controller('HomeCtrl', HomeCtrl)
    .controller('ToDosCtrl', ToDosCtrl)
    .controller('ToDosAddCtrl', ToDosAddCtrl)
    .controller('ToDosViewCtrl', ToDosViewCtrl)
    .controller('ToDosEditCtrl', ToDosEditCtrl)
    .config(ModuleConfig);