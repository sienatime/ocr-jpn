console.log("selectimage.js is a content script")

windowOpen = false;

chrome.runtime.sendMessage({greeting: "ready"}, function(response) {
  console.log(response.farewell);
});

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    console.log("i have noooooooooo idea")
    console.log(request.greeting)
    if (request.greeting == "hello"){

        var flag = false;

        if ($('.OCRJPN').css("display") == "none" ){
            $('#OCRJPNdialog').remove()
            $('.OCRJPN').remove()
        }

        if( $('.OCRJPN').length == 0 ){

            d = $('<div id="OCRJPNdialog" title="OCR-JPN"><div id="OCRJPNtext"><button id="OCRJPNocrThis">GO</button></div><div id="OCRJPNocrwindow"></div></div>');
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
                    info = $('<div id="OCRJPNkanjiinfo"></div>');
                    $('body').append(info)
                }

                loader = chrome.extension.getURL("images/loader.gif")
                $('#OCRJPNkanjiinfo').html('<img src=' + loader + '>');
            });

            flag = true;
        }
    }else if(request.greeting == "displayResults"){
        console.log("display results");
        
        $('#OCRJPNkanjiinfo').text(request.results)
    }
        sendResponse({farewell: "goodbye"});
    
  });

function printCoords(){
    console.log($('#OCRJPNocrwindow').offset().left)
    console.log($('#OCRJPNocrwindow').offset().top - $('body').scrollTop() - $('body').css('margin-top'))
    console.log($('#OCRJPNocrwindow').offset().left + $('#OCRJPNocrwindow').width())
    console.log($('#OCRJPNdialog').offset().top + $('#OCRJPNdialog').height() + parseInt($('#OCRJPNdialog').css('border-bottom').charAt(0)) - $('body').scrollTop())
}