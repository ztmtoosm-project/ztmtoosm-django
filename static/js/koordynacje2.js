var tmpl = [];

function createLine(obj, parseObj) {
    var lineAll = document.createElement("div");
    $(lineAll).append(parseObj(obj));
    var exitButton = document.createElement("a");
    exitButton.href="#";
    exitButton.innerHTML = "XX";
    exitButton.style.color="red";
    $(lineAll).append(exitButton);
    return lineAll;
}

function lineTmp(obj) {
    var xyz = document.createElement("div");
    var res = "";
    res = obj[0] + " (" + obj[1] + ") ";
    $(xyz).html(res);
    return xyz;
}

function uzup() {
    $("#uzup").empty();
    var res = "";
    for(var i=0; i<tmpl.length; i++) {
        $("#uzup").append(createLine(tmpl[i], lineTmp));
    //    res += tmpl[i][0] + " (" + tmpl[i][1] + ") " + "</br>";
    }
    //$("#uzup").html(res);
}

function replaceStopSelector(val) {
    $.get("/koordynacje/api/line_stops/"+val, function( data ) {
        $('#stopselector').empty();
        $('#startselector').empty();
        $('#endselector').empty();
        $("#btnn").prop('disabled', false);
        for(var k in data) {
            $('#stopselector').append($('<option>', {
            value: data[k].stop_id,
            text: data[k].name
            }));
        }
    });
}

$( document ).ready(function() {
    $("#btnn").prop('disabled', true);
    $.get("/koordynacje/api/all_lines/", function( data ) {
        for(var k in data) {
            $('#lineselector').append($('<option>', {
            value: data[k],
            text: data[k]
            }));
        }
    });

    $("#lineselector").change(function() {
        $( "#lineselector option:selected" ).each(function() {
            replaceStopSelector($(this).val());
            //console.log($(this).text()+" "+$(this).val());
        });
    });

    $("#stopselector").change(function() {
        $( "select option:selected" ).each(function() {
            console.log($(this).text()+" "+$(this).val());
        });
    });

    $("#btnn").click(function() {
        tmpl[tmpl.length] = [$( "#lineselector option:selected").val(), $( "#stopselector option:selected").text(), $( "#stopselector option:selected").val()];
        console.log(tmpl);
        uzup();
    });
});
