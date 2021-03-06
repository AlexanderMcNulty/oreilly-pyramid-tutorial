var React = require('react');
var ListItem = require('./ListItem.jsx');
var FlavorForm = require('./FlavorForm.jsx');
var HTTP = require('../services/httpservice');

var List = React.createClass({
    getInitialState: function() {
        return {ingredients:[]};
    },
    componentWillMount: function() {
        HTTP.get('/api/todos')
        .then(function(data) {
            this.setState({ingredients: data});
        }.bind(this));
    },
    render: function() {
        var listItems = this.state.ingredients.map(function(item) {
            return <ListItem key={item.id} ingredient={item.title} />;
        });

        return (
            <div>
                <ul>{listItems}</ul>
                <FlavorForm />
            </div>
        );
    }
});

module.exports = List;
