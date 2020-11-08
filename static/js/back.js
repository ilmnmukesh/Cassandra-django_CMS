function noBack() {
    Window.history.forward();
}

function doLogout() {
    var b = history.length;
    history.go(-b);
    window.location.replace("login/")
}