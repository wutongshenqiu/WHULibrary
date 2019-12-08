
// return hour * 60 + minute
function getNowTime() {
    let date = new Date();
    return date.getHours() * 60 + date.getMinutes();
}
