console.log("selectimage.js is a content script")

windowOpen = false;

chrome.runtime.sendMessage({greeting: "ready"}, function(response) {
  console.log(response.farewell);
});

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.greeting == "hello"){

        var flag = false;

        if ($('.OCRJPN').css("display") == "none" ){
            $('#OCRJPNdialog').remove()
            $('.OCRJPN').remove()
        }

        if( $('.OCRJPN').length == 0 ){

            d = $('<div id="OCRJPNdialog" title="OCR-JPN"><div id="OCRJPNdialogtext"><button id="OCRJPNocrThis">GO</button></div><div id="OCRJPNocrwindow"></div></div>');
            if (!flag){
                $('body').append(d);
            }
            
            $('#OCRJPNdialog').dialog();
            $('#OCRJPNocrThis').click(function(){
                var x1 = $('#OCRJPNocrwindow').offset().left
                var y1 = $('#OCRJPNocrwindow').offset().top - $('body').scrollTop()
                var x2 = $('#OCRJPNocrwindow').offset().left + $('#OCRJPNocrwindow').width()
                var y2 = $('#OCRJPNdialog').offset().top + $('#OCRJPNdialog').height() + parseInt($('#OCRJPNdialog').css('border-bottom').charAt(0) - $('body').scrollTop())
                
                chrome.runtime.sendMessage( {greeting: "capture", x1:x1, y1:y1, x2:x2, y2:y2}, function(response) {
                    $('body').append(response);
                });

                if ( $('#OCRJPNkanjiinfo').length  == 0 ){
                    info = $('<div id="OCRJPNkanjiinfo" class="OCRJPN"><button class="ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only ui-dialog-titlebar-close" role="button" aria-disabled="false" title="close" id="OCRJPNkanjiinfoclose"><span class="ui-button-icon-primary ui-icon ui-icon-closethick"></span><span class="ui-button-text">close</span></button><div id="OCRJPNtext"></div></div>');
                    $('body').append(info)
                    $( "#OCRJPNkanjiinfo" ).draggable({ cancel: "#OCRJPNtext" }); 
                    $('#OCRJPNkanjiinfoclose').click(function(){
                        $(this).parent().remove()
                    });
                }

                adjustInfoPane();
                loader = chrome.extension.getURL("images/loader.gif")
                $('#OCRJPNtext').html('<img src=' + loader + '>');
            });

            $('#OCRJPNtest').click(function(){
                takeScreenshot($('#OCRJPNocrwindow'), renderPreview)
            });

            flag = true;
        }
    }else if(request.greeting == "displayResults"){
        console.log("display results");
        adjustInfoPane();
        $('#OCRJPNtext').text(request.results);
    }
        sendResponse({farewell: "goodbye"});
    
  });

function printCoords(){
    console.log($('#OCRJPNocrwindow').offset().left)
    console.log($('#OCRJPNocrwindow').offset().top - $('body').scrollTop() - $('body').css('margin-top'))
    console.log($('#OCRJPNocrwindow').offset().left + $('#OCRJPNocrwindow').width())
    console.log($('#OCRJPNdialog').offset().top + $('#OCRJPNdialog').height() + parseInt($('#OCRJPNdialog').css('border-bottom').charAt(0)) - $('body').scrollTop())
}

function adjustInfoPane(){
    put_top = $('.OCRJPN').offset().top + 'px'
    put_left = $('.OCRJPN').offset().left + $('.OCRJPN').width() + 20 + 'px'

    console.log(put_top)
    console.log(put_left)

    $('#OCRJPNkanjiinfo').css('top', put_top);
    $('#OCRJPNkanjiinfo').css('left', put_left);
}

/* Takes a screenshot and uses it in a callback as a canvas */

takeScreenshot = function($element, callback) {
    chrome.extension.sendMessage({name: 'screenshot'}, function(response) {
        var data = response.screenshotUrl;
        var canvas = document.createElement('canvas');
        var img = new Image();
        img.onload = function() {
            canvas.width = $(window).width();
            canvas.height = $(window).height()
            canvas.getContext("2d").drawImage(img, 0, 0);

            var $canvas = $(canvas);
            $canvas.data('scrollLeft', $(document.body).scrollLeft());
            $canvas.data('scrollTop', $(document.body).scrollTop());

            $('body').append($canvas)
            // Perform callback after image loads
            $('body').append(callback($element, $canvas));
        }
        img.src = data;
    });
}

/* Returns a canvas containing a screenshot of $element */
renderPreview = function($element, $screenshotCanvas) {

    var previewCanvas = document.createElement('canvas');
    var height = $('#OCRJPNdialog').height() - $('#OCRJPNdialogtext').height()

    previewCanvas.width = $element.width() - 3;
    previewCanvas.height = height;

    // Calculate the correct position of the element on the canvas
    var prevTop = $element.offset().top - $screenshotCanvas.data('scrollTop');
    var prevLeft = $element.offset().left - $screenshotCanvas.data('scrollLeft');

    console.log($element.width())
    console.log(height)

  // in nsIDOMElement image,
  // in float sx,
  // in float sy,
  // in float sw,
  // in float sh,
  // in float dx, 
  // in float dy,
  // in float dw,
  // in float dh

  //where the d letters are x, y position, width and height, and the s positions are the 'sub rectangles' aka the crop position.
  // the screenshot is of the entire tab, so the first 4 numbers would make sense to be the same as the numbers i've been using.

    var ctx = previewCanvas.getContext("2d");
    ctx.drawImage($screenshotCanvas[0], prevLeft, prevTop,
                                        $element.width(), height,
                                        0, 0,
                                        $element.width() - 3, height);

    return $(previewCanvas)
                .css({ border:'1px solid black' });
}