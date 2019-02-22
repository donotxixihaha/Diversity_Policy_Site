$(document).ready(function() {
    var timeoutID = null;
    function findMember(str) {
        console.log('search: ' + str);
    }
    $('#s_bar2').keyup(function(err) {
        var query = $("#s_bar2").val();
        clearTimeout(timeoutID);
        $.ajax({
            url: "/policy_suggest/?search=" + query,
            type: 'GET',
            dataType: 'json',
            success: function(res) {
                //console.log(res);
                var tags = res.suggestions;
                console.log(tags);
                $( "#s_bar2" ).autocomplete({
                    source: tags
                });
            }
        });
        //console.log("handler function called! Data: " + query);
    });
});

function testJS() {
    var query = document.getElementById("s_bar2").value;
    sessionStorage.setItem("storing", query);
}