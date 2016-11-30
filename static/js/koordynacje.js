var tmpl = [];

function uzup() {
    var res = "";
    for(var i=0; i<tmpl.length; i++) {
        res += tmpl[i][0] + " > " + tmpl[i][1] + " > " + tmpl[i][2] + "</br>";
    }
    $("#uzup").html(res);
}

function replaceTripSelector(val) {
    $.get("/koordynacje/api/line_directions/"+val, function( data ) {
        $('#tripselector').empty();
        $('#startselector').empty();
        $('#endselector').empty();
        $("#btnn").prop('disabled', false);
        for(var k in data) {
            $('#tripselector').append($('<option>', {
            value: k,
            text: data[k]
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
            replaceTripSelector($(this).val());
            //console.log($(this).text()+" "+$(this).val());
        });
    });

    $("#tripselector").change(function() {
        $( "select option:selected" ).each(function() {
            console.log($(this).text()+" "+$(this).val());
        });
    });

    $("#btnn").click(function() {
        tmpl[tmpl.length] = [$( "#lineselector option:selected").val(), $( "#tripselector option:selected").text(), $( "#tripselector option:selected").val()];
        console.log(tmpl);
        uzup();
        $.post("/koordynacje/api/get_tree/", {"trips" : JSON.stringify(tmpl)}, function(data) {

            var tablen = data[0].length;
            var ttt2 = "";
            for(var i=3; i<tablen; i+=20)
            {
                var ttt = "<table class='table-bordered'>";
                for(var z in data)
                {
                    var tttmp = "<tr>";
                    for(var j=0; j<2; j++)
                    {
                        tttmp += "<td>" + data[z][j] + "</td>";
                    }
                    for(var j=i; j<(i+20); j++)
                    {
                        tttmp += "<td>" + data[z][j] + "</td>";
                    }
                    tttmp += "</tr>"
                    ttt += tttmp;
                }
                ttt += "</table>"
                ttt2 += ttt;
            }
            $("#lilb").html(ttt2);
        });
    });
});
