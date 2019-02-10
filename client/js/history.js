function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}
$(document).ready(function () {
    console.log("ready");

    $.ajax({
        type: "GET",
        dataType: "json",
        url: "http://54.160.238.67:5000/history",
        cache: false,
        success: function (data) {
            

            console.log(data['Count']);

            data['Items'].sort(function (a, b) {
                if (a.dateandtime < b.dateandtime) {
                    return 1;
                } else if (a.dateandtime > b.dateandtime) {
                    return -1;
                } else {
                    return 0;
                }
            });
            var i;
            for (i = 0; i < data['Count']; i++) {
                var s = '<div class="item">' +
                    '<p> <b>Name: </b>' + data['Items'][i]['name'] + '<br></p>' +
                    '<img src="' + data['Items'][i]['url'] + '"  width="200" height="200">' +
                    '<p> <b>Date And Time: </b>' + data['Items'][i]['dateandtime'] + '<br></p>' +
                    '<p> <b>Status: </b>' + data['Items'][i]['status'] + '<br></p>' +
                    
                    ' </div > ';
                $("#division").append(s + "<br>");

            };


        }
    });
});