var date = new Date();
var year = date.getFullYear();
var mon = date.getMonth()
var day = date.getDate()
if (mon.toString().length == 1)
    mon = '0' + mon;
if (day.toString().length < 2)
    day = '0' + day;

values = year + '-' + mon + '-' + day;
world()
document.getElementById('date').value = value;

function world() {
    var myDate = document.querySelector(date);
    var today = new Date();
    myDate.value = dates.toISOString().substr(0, 10);
}