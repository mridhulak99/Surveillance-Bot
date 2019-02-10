function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}
$(document).ready(function () {
    console.log("ready");
    $.ajax({
        type: "POST",
        data: '{"hi":"hi"}',
        dataType: "json",
        url: "http://54.160.238.67:5000/users",
        cache: false,
        success: function (data) {
            console.log(data);
            console.log(data['Items']);

            var i;
            for (i = 0; i < data['Count']; i++) {
                var s = '<div class="item">' +

                    '<p> <b>Name: </b>' + data['Items'][i]['name'] + '<br></p>' +
                    '<img src="' + data['Items'][i]['url'] + '" width="200" height="200">' +

                    ' </div > ';
                $("#division").append(s + "<br>");

            };


        }
    });
});
