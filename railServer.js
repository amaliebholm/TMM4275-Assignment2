$(function() {
    generate();
    clear();
    logNumber();
});

function generate() {
    $("#generateButton").on("click", function() {
        var value = parseInt($("#size").val());
        if (value > 20 || value < 1) {
            alert("Please select a number betweeen 1 and 20!");
            return;
        }
        var content = "";
        var num = 1;
        for (var i = 1; i <= value; i++) {
            for (var j = 1; j <= value; j++) {
                if (j === 1) {
                    content += "<div class='row'><div class='grid'>" + num + "</div>";
                } else if (j === value) {
                    content += "<div class='grid'>" + num + "</div></div>";
                } else {
                    content += "<div class='grid'>" + num + "</div>";
                }
                num++;
            }
        }
        $("#grids").html(content);
    });
}

//Event delegation
function logNumber() {
    $("#grids").on("click", ".grid", function() {
        var value = $(this).text();
        alert("You click "  +value);
    });
}

function clear() {
    $("#clearButton").on("click", function() {
        $("#grids").html(" ");
    });
}