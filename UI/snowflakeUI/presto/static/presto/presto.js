// JavaScript source code

$(document).ready(function () {
    $("#AJAX_get").click(function () {
        var info = $("#info").val();
        var data = { "info": info };
        $.get(
            '/presto/ajax_get',
            data,
            function (ret) {
                var info = ret['info'];
                let map = new Map();
                $.each(info, function (idx, elem) {
                    if (map[elem[0]] === undefined) {
                        map[elem[0]] = [elem[1]];
                    }
                    else
                        map[elem[0]].push(elem[1]);
                });
                var myList = $("ul.mylist");
                myList.children().remove();
                for (var s in map) {
                    var li = $("<li>" + s + "</li>").appendTo(myList);
                    var ul = $("<ul/>").appendTo(li);
                    for (var i = 0; i < map[s].length; i++) {
                        ul.append($("<li><a href='#' class="  + s + ">" + map[s][i] + "</a></li>"));
                    }
                }
            })
    });

    $("#AJAX_query").click(function () {
        var info = $("#info_query").val();
        var data = { "info": info };
        console.log(info);

        $.get(
            '/presto/ajax_query',
            data,
            function (ret) {
                var info = ret['info'];
                var table = $("#table tbody");
                table.children().remove()
                $.each(info, function (idx, elem) {
                    table.append("<tr><td>" + elem + "</td></tr>");
                })
            })
    });

    $(document).on("click", "a", function () {
        var command = "describe " + $(this).attr('class') + "." + $(this).text();
        var data = { "command": command };
        $.get(
            '/presto/ajax_describe',
            data,
            function (ret) {
                var results = ret['results'];
                var table = $("#table_e tbody");
                table.children().remove()
                $.each(results, function (idx, elem) {
                    table.append("<tr><td>" + elem + "</td></tr>");
                })
            })
    });
});