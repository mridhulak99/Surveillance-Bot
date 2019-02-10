function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}
$(document).ready(function () {
    console.log("ready");

    $("#upload").click(function () {
        console.log("clicked");
        var blobFile = $('#filechooser').files;
        var formData = new FormData();
        formData.append("fileToUpload", blobFile);
        $.ajax({
            url: "http://54.160.238.67:5000/adduser",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            crossOrigin: null,
            crossDomain: true
        })
            .done(function (data) {
                if (data.error) {
                    console.log(data.Outcome);

                }
                else {
                    console.log(data);
                }
            });
            

        });
    
 });