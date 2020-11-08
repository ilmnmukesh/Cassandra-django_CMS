function standby() {
    document.getElementById('blah').src = "/static/image/logo_cat.png";
}


function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            $('#blah')
                .attr('src', e.target.result)
                .width(150)
                .height(180);
        };
        reader.readAsDataURL(input.files[0]);
    }
}
var selDiv = "";
document.addEventListener('DOMContentLoaded', init, false);

function init() {
    document.querySelector('#files').addEventListener('change', handleFileSelect, false);
    selDiv = document.querySelector("#selectedFile");
}

function handleFileSelect(e) {
    if (!e.target.files) return;
    selDiv.innerHTML = "";
    var files = e.target.files;
    for (var i = 0; i < files.length; i++) {
        var f = files[i];
        selDiv.innerHTML += f.name + "<br>";

    }
}