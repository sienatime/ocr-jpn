
coords = []

// $(function() {
    
//   });

$(document).ready(function() {

    $( "#OCRJPNdialog" ).dialog();

    info = $('<div id="OCRJPNkanjiinfo" class="OCRJPN"><button class="ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only ui-dialog-titlebar-close" role="button" aria-disabled="false" title="close" id="OCRJPNkanjiinfoclose"><span class="ui-button-icon-primary ui-icon ui-icon-closethick"></span><span class="ui-button-text">close</span></button><div id="OCRJPNtext"></div></div>');
    $('body').append(info)
    $( "#OCRJPNkanjiinfo" ).draggable({ cancel: "#OCRJPNtext" });

    $('#OCRJPNkanjiinfoclose').click(function(){
        $(this).parent().remove()
    });

    adjustInfoPane();

    $('#OCRJPNtext').html('<img src="images/loader.gif">'); 


    $('#OCRJPNocrThis').click(function(){
        $('#OCRJPNtext').html("Here's me faking some stuff")
    });


});

function adjustInfoPane(){
    put_top = $('.OCRJPN').offset().top + 'px'
    put_left = $('.OCRJPN').offset().left + $('.OCRJPN').width() + 20 + 'px'

    $('#OCRJPNkanjiinfo').css('top', put_top);
    $('#OCRJPNkanjiinfo').css('left', put_left);
}


function printCoords(){
    console.log($('#OCRJPNocrwindow').offset().left)
    console.log($('#OCRJPNocrwindow').offset().top)
    console.log($('#OCRJPNocrwindow').offset().left + $('#OCRJPNocrwindow').width())
    console.log($('#OCRJPNdialog').offset().top + $('#OCRJPNdialog').height() + parseInt($('#OCRJPNdialog').css('border-bottom').charAt(0)))
}