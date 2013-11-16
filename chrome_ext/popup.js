console.log("popup.js")
// chrome.runtime.sendMessage({greeting: "screenshot"}, function(response) {
//     console.log("sending message chrome.runtime.sendMessage")
//     console.log(response.screenshotUrl);
// });



chrome.tabs.captureVisibleTab(null, null, function(dataUrl) {

            // screenshot = dataUrl;
            console.log(dataUrl)

            // chrome.tabs.sendRequest(tabId, {
            //                          'action': 'createCanvas',
            //                          'data'  : {'dataUrl' : dataUrl}
            //                          });
        });

