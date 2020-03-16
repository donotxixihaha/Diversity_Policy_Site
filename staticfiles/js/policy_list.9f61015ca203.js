$(document).ready(function() {

    $(".school_name").each(function(){
        $(this).text($(this).text().toTitleCase());
    });

    $(".card-title").each(function(){
        $(this).text($(this).text().toTitleCase());
    });

    $("#loader").hide();

    // Year filter dropdown
    $(".panel").click(function(){
        var icon = document.querySelector(".icon");
        if(document.querySelector("#toggle").checked == false) {
            icon.innerHTML = "–";
        } else {
            icon.innerHTML = "+";
        }
    });

    // School filter dropdown
    $(".panel-two").click(function(){
        var two = document.querySelector(".icon-two");
        if(document.querySelector("#toggle-two").checked == false) {
            two.innerHTML = "–";
        } else {
            two.innerHTML = "+";
        }
    });

    $(".panel-three").click(function(){
        var three = document.querySelector(".icon-three");
        if(document.querySelector("#toggle-three").checked == false) {
            three.innerHTML = "–";
        } else {
            three.innerHTML = "+";
        }
    });

    var timeoutID = null;
    // function findMember(str) {
    //     console.log('search: ' + str);
    // }


    // Search bar autocomplete suggestions
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
                // console.log(tags);
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
    $('.query').each(function(){
        $(this).val(urlParams.get('search'));
    });

    // Filters
    var years = [];
    var schools = [];
    var states = [];
    $('.filter').each(function(){
        if(this.getAttribute("data-year") != null){
            var year = this.getAttribute("data-year").split(" ");
            key = year[2];
            this.setAttribute('data-year', key)
             if(!years.includes(key)){
                years.push(key);
                $(this).val(key);
            } else {
                $(this).remove();
            }
        }
        if(this.getAttribute("data-school") != null){
            var school = this.getAttribute("data-school").trim();
            if(!schools.includes(school)){
                schools.push(school);
            } else {
                $(this).remove();
            }
        }
        if(this.getAttribute("data-state") != null){
            var state = this.getAttribute("data-state").trim();
            if(!states.includes(state)){
                states.push(state);
            } else {
                $(this).remove();
            }
        }
    });

    // Filter labels (years and school names)
    $('.filter').each(function(){
        $(this).wrap("<label></label>");
        if(this.getAttribute("data-school") != null){
            $(this).val(this.getAttribute("data-school").toLowerCase());
        }
    });

    $('.dropdown label').each(function(){
        var yr = $(this).find("input").val();
        this.innerHTML += "<span> " + yr + "</span>";
    });

    $('.dropdown-two label').each(function(){
        var school = $(this).find("input").val().toTitleCase();
        this.innerHTML += "<span> " + school + "</span>";
    });

    $('.dropdown-three label').each(function(){
        var state = $(this).find("input").data("state").toTitleCase();
        this.innerHTML += "<span> " + state + "</span>";
    });


    // Load/unload filtered content without page refresh
    var filter_url = window.location.search;
    $( ".filter" ).on( "click", function( event ) {
        var str = "&filter=" + this.getAttribute("data-year");
        if(this.getAttribute("data-school") != null) {
            var school = encodeURIComponent(this.getAttribute("data-school").toLowerCase().trim());
            var str2 = "&filter=" + school;
        }
        if(this.getAttribute("data-state") != null) {
            var state = encodeURIComponent(this.value.toLowerCase().trim());
            var str3 = "&filter=" + state;
        }
        if($(this).prop("checked") == false) {
            $("#loader").show();
            filter_url = filter_url.replace(str, "");
            filter_url = filter_url.replace(str2, "");
            filter_url = filter_url.replace(str3, "");
            window.history.pushState({}, null, filter_url);
            $("#results").load(filter_url + " #results", function(){
                $("#loader").hide();
                $(".card-title").each(function(){
                    $(this).text($(this).text().toTitleCase());
                });
                $(".school_name").each(function(){
                    $(this).text($(this).text().toTitleCase());
                });
                $(window).scrollTop(0);
            });
        }
        else {
            $("#loader").show();
            filter_url += ("&" + $(this).serialize());
            window.history.pushState({}, null, filter_url);
            $("#results").load(filter_url + " #results", function(){
                $("#loader").hide();
                $(".card-title").each(function(){
                    $(this).text($(this).text().toTitleCase());
                });
                $(".school_name").each(function(){
                    $(this).text($(this).text().toTitleCase());
                });
                $(window).scrollTop(0);
            });
        }
    });

    // Temp fix for back button not loading previous content after a filter is checked
    $(window).on("popstate", function (e) {
        location.reload();
    });

    // Scroll to top of results after navigating to a new page
    $(document).on("click", ".pagination a", function( event ) {
        $("#loader").show();
        event.preventDefault();
        window.history.pushState({}, null, this.href);
        $("#results").load(this.href + " #results", function(){
            $("#loader").hide();
            $(".card-title").each(function(){
                $(this).text($(this).text().toTitleCase());
            });
            $(".school_name").each(function(){
                $(this).text($(this).text().toTitleCase());
            });
            $(window).scrollTop(0);
        });
    });

});

// Sort filter labels
var yearFilter = document.querySelectorAll("[data-year]");
var yearFilterArray = Array.from(yearFilter);
let sorted = yearFilterArray.sort(sorter);
// console.log(sorted)
function sorter(a,b) {
    if(a.dataset.year.split(" ")[2] < b.dataset.year.split(" ")[2] ) {
        return -1;
    }
    if(a.dataset.year > b.dataset.year) {
        return 1;
    }
}
sorted.forEach(e => document.querySelector("#yr-filter > form").appendChild(e));


var schoolFilter = document.querySelectorAll("[data-school]");
var schoolFilterArray = Array.from(schoolFilter);
for(let i=0; i < schoolFilterArray.length; i++){
    schoolFilterArray[i].setAttribute("data-school", schoolFilterArray[i].getAttribute("data-school").toTitleCase());
}
let sorted2 = schoolFilterArray.sort(sorter2);
function sorter2(a,b) {
    if(a.dataset.school < b.dataset.school) return -1;
    if(a.dataset.school > b.dataset.school) return 1;
}
sorted2.forEach(e => document.querySelector("#school-filter > form").appendChild(e));


var stateFilter = document.querySelectorAll("[data-state]");
var stateFilterArray = Array.from(stateFilter);
for(let i=0; i < stateFilterArray.length; i++){
    stateFilterArray[i].setAttribute("data-state", stateFilterArray[i].getAttribute("data-state").toTitleCase());
}
let sorted3 = stateFilterArray.sort(sorter3);
function sorter3(a,b) {
    if(a.dataset.state < b.dataset.state) return -1;
    if(a.dataset.state > b.dataset.state) return 1;
}
sorted3.forEach(e => document.querySelector("#state-filter > form").appendChild(e));

// Copy link button
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

function CopyToClipboard(id, link) {
    copyTextToClipboard(link);
    var elem = document.getElementById(id);
    $(elem).val($(elem).data("loading-text")); setTimeout(function(){
        $(elem).val('Copy Link');
    }, 1500);
}


// Citations
function showCites(source) {
    // Get the modal
    var modal = document.getElementById('myModal');

    // Get the button that opens the modal
    var btn = document.getElementById("myBtn");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    modal.style.display = "block";

    document.getElementById('mla').innerHTML = getMLA(source);
    document.getElementById('apa').innerHTML = getAPA(source);
    document.getElementById('chicago').innerHTML = getChicago(source);

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
      modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
}

function getMLA(source) {
    var mla = "";
    if(source.getAttribute("data-author").length > 2 && source.getAttribute("data-author") != "None") {
        mla += (formatAuthor(source.getAttribute("data-author").trim(), "mla"));
    }
    if(source.getAttribute("data-title")) {
        var title = source.getAttribute("data-title").split(" ");
        if(title[title.length-1].includes("?") || title[title.length-1].includes("!")
        || title[title.length-1].includes(".")) {
            mla += ('"' + source.getAttribute("data-title").trim() + '" ');
        } else {
            mla += ('"' + source.getAttribute("data-title").trim() + '." ');
        }
    }
    if(source.getAttribute("data-publisher")) {
        var pub = source.getAttribute("data-publisher").trim().toTitleCase();
        mla += (pub.italics() + ', ');
    }
    if(source.getAttribute("data-pubdate") && source.getAttribute("data-pubdate") != "None") {
        mla += (formatDate(source.getAttribute("data-pubdate").trim(), "mla") + ", ");
    }
    var url = source.getAttribute("data-url");
    url = url.replace(/^\/\/|^.*?:(\/\/)?/, '');
    mla += url.trim() + ". ";

    var date = new Date();
    var months = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."];
    var day = date.getDate();
    var monthIndex = date.getMonth();
    var year = date.getFullYear();
    mla += "Accessed " + day + ' ' + months[monthIndex] + ' ' + year + ".";

    return mla;
}

function getAPA(source) {
    var apa = "";
    if(source.getAttribute("data-author").length > 2 && source.getAttribute("data-author") != "None") {
        apa += (formatAuthor(source.getAttribute("data-author").trim(), "apa"));
    }
    if(source.getAttribute("data-title")) {
        var title = source.getAttribute("data-title").split(" ");
        if(title[title.length-1].includes("?") || title[title.length-1].includes("!")
        || title[title.length-1].includes(".")) {
            apa += (source.getAttribute("data-title").trim() + ' ');
        } else {
            apa += (source.getAttribute("data-title").trim() + '. ');
        }
    }
    if(source.getAttribute("data-pubdate") && source.getAttribute("data-pubdate") != "None") {
        apa += ("(" + formatDate(source.getAttribute("data-pubdate").trim(), "apa") + "). ");
    } else {
        apa += "(n.d.). ";
    }

    apa += "Retrieved from " + source.getAttribute("data-url");
    return apa;
}

function getChicago(source) {
    var chicago = "";
    if(source.getAttribute("data-author").length > 2 && source.getAttribute("data-author") != "None") {
        chicago += (formatAuthor(source.getAttribute("data-author").trim(), "chicago"));
    }
    if(source.getAttribute("data-title")) {
        var title = source.getAttribute("data-title").split(" ");
        if(title[title.length-1].includes("?") || title[title.length-1].includes("!")
        || title[title.length-1].includes(".")) {
            chicago += ('"' + source.getAttribute("data-title").trim() + '" ');
        } else {
            chicago += ('"' + source.getAttribute("data-title").trim() + '." ');
        }
    }
    if(source.getAttribute("data-publisher")) {
        chicago += (source.getAttribute("data-publisher").trim() + '. ').toTitleCase();
    }
    if(source.getAttribute("data-pubdate") && source.getAttribute("data-pubdate") != "None") {
        chicago += (formatDate(source.getAttribute("data-pubdate").trim(), "chicago") + '. ');
    } else {
        var date = new Date();
        var months2 = ["January", "February", "March", "April", "May", "June", "July", "August",
            "September", "October", "November", "December"];
        var day = date.getDate();
        var monthIndex = date.getMonth();
        var year = date.getFullYear();
        chicago += "Accessed " + months2[monthIndex] + ' ' + day + ', ' + year + ". ";
    }

    chicago += source.getAttribute("data-url");
    return chicago;
}

function formatAuthor(author, format) {
    if(format == "mla" || format == "chicago") {
        var formatted = author.split(" ");
        if(formatted.length == 3) {
            if(formatted[1].includes(".")) {
                return formatted[2] + ', ' + formatted[0] + ' ' + formatted[1] + " ";
            }
            return formatted[2] + ', ' + formatted[0] + ' ' + formatted[1] + ". ";
        } else {
            return formatted[1] + ', ' + formatted[0] + ". ";
        }
    }
    else if(format == "apa") {
        var formatted = author.split(" ");
        if(formatted.length == 3) {
            return formatted[2] + ", " + formatted[0][0] + ". " + formatted[1] + " ";
        }
        else {
            return formatted[1] + ", " + formatted[0][0] + ". ";
        }
    }
}

function formatDate(date, format) {
    var pubdate = new Date(date);
    pubdate = new Date( pubdate.getTime() - pubdate.getTimezoneOffset() * -60000 );
    var day = pubdate.getDate();
    var month = pubdate.getMonth();
    var year = pubdate.getFullYear();
    var months = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.",
            "Sept.", "Oct.", "Nov.", "Dec."];
    var months2 = ["January", "February", "March", "April", "May", "June", "July", "August",
            "September", "October", "November", "December"];

    if(date.split("-").length == 1) {
        return year
    }
    else if(date.split("-").length == 2) {
        if(format == "mla") {
            return months[month] + ' ' + year;
        }
        else if(format == "apa") {
            return year + ", " + months2[month];
        }
        else {
            return months2 + ", " + year;
        }
    }
    else if(date.split("-").length == 3) {
        if(format == "mla") {
            return day + ' ' + months[month] + ' ' + year;
        }
        else if(format == "apa") {
            return year + ", " + months2[month] + " " + day;
        }
        else {
            return months2[month] + " " + day + ", " + year;
        }
    }
    else {}
}


// Bold search term(s) in abstract – does not work for multi-word queries
$(document).ready(function() {
    var keyword = $("#s_bar2").val();
    var abstracts = [];
    var desc = document.getElementsByClassName('abstract');
    for(var i = 0, len = desc.length; i < len; i++) {
        if(desc[i].innerHTML.indexOf(keyword) !== -1) {
            abstracts.push(desc[i]);
        }
    }
    var result = "";
    for(abs in abstracts) {
        var text = abstracts[abs].innerHTML;
        var regex = new RegExp(keyword, 'g');
        result += text.replace(regex, '<b>' + keyword +'</b>');
        result += "|"
    }
    var abstracts_new = result.split("|");
    var j = 0;
    for(var i = 0, len = desc.length; i < len; i++) {
        if(desc[i].innerHTML.indexOf(keyword) !== -1) {
            desc[i].innerHTML = abstracts_new[j];
            j++;
        }
    }
});

function openNav() {
    document.getElementById("aside").style.width = "100%";
}
function closeNav() {
    document.getElementById("aside").style.width = "0";
}