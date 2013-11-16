console.log("popup.js")
// chrome.runtime.sendMessage({greeting: "screenshot"}, function(response) {
//     console.log("sending message chrome.runtime.sendMessage")
//     console.log(response.screenshotUrl);
// });



chrome.tabs.captureVisibleTab(null, {format: "png"}, function(dataUrl) {

            // screenshot = dataUrl;
            console.log(dataUrl)

            // chrome.tabs.sendRequest(tabId, {
            //                          'action': 'createCanvas',
            //                          'data'  : {'dataUrl' : dataUrl}
            //                          });

            $.ajax({
              type: "POST",
              url: "http://127.0.0.1:5000/makeimage",
              data: { dataUrl : dataUrl }
            })
              .done(function( msg ) {
                alert( "Data Saved: " + msg );
              });

        });

