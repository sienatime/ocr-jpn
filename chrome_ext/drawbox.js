
coords = []

// $(function() {
    
//   });

$(document).ready(function() {
    $( "#OCRJPNdialog" ).dialog();

    info = $('<div id="OCRJPNkanjiinfo">Here\'s some info</div>');

    $('body').append(info)

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