
coords = []

// $(function() {
    
//   });

$(document).ready(function() {

    $( "#OCRJPNdialog" ).dialog();

    info = $('<div id="OCRJPNinfotitle">OCR Results</div><div id="OCRJPNkanjiinfo">Here\'s some info</div>');

    $('body').append(info)

    $( "#OCRJPNinfotitle" ).draggable();
    put_top = $('.OCRJPN').offset().top + 'px'
    put_left = $('.OCRJPN').offset().left + $('.OCRJPN').width() + 20 + 'px'

    $('#OCRJPNkanjiinfo').css('top', put_top);
    $('#OCRJPNkanjiinfo').css('left', put_left);

    $('#OCRJPNkanjiinfo').html('<img src="images/loader.gif">');

    $('#OCRJPNocrThis').click(function(){
        $('#OCRJPNkanjiinfo').html("Here's me faking some stuff")
    });


});

function printCoords(){
    console.log($('#OCRJPNocrwindow').offset().left)
    console.log($('#OCRJPNocrwindow').offset().top)
    console.log($('#OCRJPNocrwindow').offset().left + $('#OCRJPNocrwindow').width())
    console.log($('#OCRJPNdialog').offset().top + $('#OCRJPNdialog').height() + parseInt($('#OCRJPNdialog').css('border-bottom').charAt(0)))
}