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

    $(".navbar a").on('click', function(event) {
    if (this.hash !== "") {
        event.preventDefault();
        var hash = this.hash;
        $('html, body').animate({
            scrollTop: $(hash).offset().top
        }, 800, function(){
            window.location.hash = hash;
        });
    }
});

});
