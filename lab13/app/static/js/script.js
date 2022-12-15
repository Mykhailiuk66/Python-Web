function setLocalTimezone(){
    $(".time-utc").each(function () {
        console.log($(this).text());

        if ($(this).text() != "None") {
            var utcTime = $(this).text() + " UTC";
            var date = new Date(utcTime);
            date = date.toLocaleString();
        }
        else {
            var date = "-"
        }

        $(this).text(date);
        $(this).removeClass("time-utc");
    });
}