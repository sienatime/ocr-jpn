console.log("background.js")

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {

    if (request.greeting == "capture"){
        console.log("doing stuff")
        chrome.tabs.captureVisibleTab(null, {format: "png"}, function(dataUrl) {
        console.log(request.x1)

        $.ajax({
          type: "POST",
          url: "http://127.0.0.1:5000/makeimage",
          data: { dataUrl : dataUrl, x1:request.x1, y1:request.y1, x2:request.x2, y2:request.y2 }
        })
          .done(function( msg ) {
                chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                  chrome.tabs.sendMessage(tabs[0].id, {greeting: "displayResults", results: msg}, function(response) {
                      //this will only get run if you try to click the button before the page is done loading.
                      console.log("response")
                  });
              });
          });

    });
    }else if (request.name == 'screenshot') {
      console.log("received screenshot message")
        chrome.tabs.captureVisibleTab(null, null, function(dataUrl) {
            sendResponse({ screenshotUrl: dataUrl });
        });
    }
    return true;
});


