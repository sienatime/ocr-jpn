console.log("selectimage.js is a content script")

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    console.log("i have noooooooooo idea")
    console.log(request.greeting)
    if (request.greeting == "hello"){
        d = $('<div id="dialog"><p><button id="ocrThis">OCR-JPN</button></p><div id="ocrwindow"></div></div>')
        $('body').append(d)
        $('#dialog').dialog();

        $('#ocrThis').click(function(){
            var x1 = $('#ocrwindow').offset().left
            var y1 = $('#ocrwindow').offset().top
            var x2 = $('#ocrwindow').offset().left + $('#ocrwindow').width()
            var y2 = $('#dialog').offset().top + $('#dialog').height()
            
            chrome.runtime.sendMessage( {greeting: "capture", x1:x1, y1:y1, x2:x2, y2:y2}, function(response) {
                console.log(response)
            });
        });
      sendResponse({farewell: "goodbye"});
    }
  });

function printCoords(){
    console.log($('#ocrwindow').offset().left)
    console.log($('#ocrwindow').offset().top)
    console.log($('#ocrwindow').offset().left + $('#ocrwindow').width())
    console.log($('#dialog').offset().top + $('#dialog').height())
}