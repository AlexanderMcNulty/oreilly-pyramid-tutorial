$(document).ready(function () {
    // register an event handler, on the html element
     $("#name").change(function () {
            var newValue = $("#name").val();
            $.ajax({
                method: "POST",
                url: "/",
                // stringify the data we are going to send
                data: JSON.stringify({name: newValue}),
                // set the data type to
                contentType: 'application/json; charset=utf-8'
                //this will trigger json underbody support
            }).done(
                // assign its text value the return value
                function (data) {
                    $('#greeting').text(data.greeting);
                }
            );
        });
})
;
