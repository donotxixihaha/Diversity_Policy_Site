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

    //Save previous search query in the current search bar--get from URL
    //Problem is that there is a tiny lag before it appears
    const urlParams = new URLSearchParams(window.location.search);
    $('#s_bar2').val(urlParams.get('search'));
});

function fallbackCopyTextToClipboard(text) {
    var textArea = document.createElement("textarea");
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'successful' : 'unsuccessful';
        console.log('Fallback: Copying text command was ' + msg);
    } catch (err) {
        console.error('Fallback: Oops, unable to copy', err);
    }

    document.body.removeChild(textArea);
}

function copyTextToClipboard(text) {
    if (!navigator.clipboard) {
        fallbackCopyTextToClipboard(text);
        return;
    }
    navigator.clipboard.writeText(text).then(function() {
        console.log('Async: Copying to clipboard was successful!');
    }, function(err) {
        console.error('Async: Could not copy text: ', err);
    });
}

function CopyToClipboard(link) {
    copyTextToClipboard(link);
};

window.onload = function () {
//    const urlParams = new URLSearchParams(window.location.search);
//    $('#s_bar2').val(urlParams.get('search'));
}