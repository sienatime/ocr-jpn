
coords = []

// $(function() {
    
//   });

$(document).ready(function() {

    $( "#OCRJPNdialog" ).dialog();

    info = $('<div id="OCRJPNkanjiinfo" class="OCRJPN"><button class="ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only ui-dialog-titlebar-close" role="button" aria-disabled="false" title="close" id="OCRJPNkanjiinfoclose"><span class="ui-button-icon-primary ui-icon ui-icon-closethick"></span><span class="ui-button-text">close</span></button><div id="OCRJPNtext"></div></div>');


    $('body').append(info)
    $( "#OCRJPNkanjiinfo" ).draggable({ cancel: "#OCRJPNtext" });

    $('#OCRJPNkanjiinfo').mouseleave(function(){
        $('.candidateWrapper').css('display','none');
    })

    $('#OCRJPNkanjiinfoclose').click(function(){
        $(this).parent().remove()
    });

    

    // $('#OCRJPNtext').html('<img src="images/henoheno.gif">'); 

    $( "#OCRJPNocrThis" ).button({ icons: { primary: "ui-icon-check" }});


    $('#OCRJPNocrThis').click(function(){
        $('#OCRJPNtext').html("");
        // don't parse the JSON--$.ajax did it for you
        var candidates = [['\u65e5','\u30e8','\u30ed'],['\u672c','\u30cd','\u6728']]

        for (var i = 0; i < candidates.length; i++) {
            var characters = candidates[i]
            // maybe make a span or something that has an ID and then put the 0 element in that span
            // then you can do stuff with the other things.
            var id = "chara" + i
            var chara = $('<span id="' + id + '" class="OCRJPNresult"></span>')
            
            var candidate_wrapper = $('<div id="candidateWrapper'+ i + '" class="candidateWrapper"></div>')

            for (var j = 1; j < characters.length; j++) {
                var candSpan = $('<span id="'+ id + 'candidate'+ j + '" class="OCRJPNcandidate"></span>')
                candSpan.text(characters[j])
                candSpan.click(swapChars)
                candidate_wrapper.append(candSpan)
            };

            chara.text(candidates[i][0])
            
            chara.click(function(){
                $('.candidateWrapper').css('display','none')
                id = this.id[5] //ugh this is so bad
                $('#candidateWrapper'+id).css('display', 'block')
            })
            $('#OCRJPNtext').append(chara);
            $('#OCRJPNtext').append(candidate_wrapper);
        };
        
    });

    $('.OCRJPN.ui-dialog').resize(function(){
        // LOL THIS IS WHY I DIDN'T WANT TO DO THIS
        height = $('#OCRJPNdialog').height() - $('.OCRJPN.ui-dialog #OCRJPNdialogtext').height() - parseInt( $('#OCRJPNwindowwrapper').css('border-bottom') ) - parseInt( $('#OCRJPNwindowwrapper').css('border-top') ) - parseInt( $('#OCRJPNocrwindow').css('border-bottom') ) - parseInt( $('#OCRJPNocrwindow').css('border-top') );
        $('#OCRJPNocrwindow').height(height)
    });

    adjustInfoPane();

});

swapChars = function(){
    id = this.id[5]
    swap = $('#chara'+id).text()
    $('#chara'+id).text(this.innerHTML)
    this.innerHTML = swap
}

function adjustInfoPane(){
    put_top = $('.OCRJPN.ui-dialog').offset().top + 'px'
    put_left = $('.OCRJPN.ui-dialog').offset().left + $('.OCRJPN.ui-dialog').width() + 20 + 'px'

    $('#OCRJPNkanjiinfo').css('top', put_top);
    $('#OCRJPNkanjiinfo').css('left', put_left);
    $('#OCRJPNkanjiinfo').css('position', 'absolute');
}


function printCoords(){
    console.log($('#OCRJPNocrwindow').offset().left)
    console.log($('#OCRJPNocrwindow').offset().top)
    console.log($('#OCRJPNocrwindow').offset().left + $('#OCRJPNocrwindow').width())
    console.log($('#OCRJPNdialog').offset().top + $('#OCRJPNdialog').height() + parseInt($('#OCRJPNdialog').css('border-bottom').charAt(0)))
}