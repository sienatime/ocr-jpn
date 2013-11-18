console.log("popup.js")

function openDialog(){
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {greeting: "hello"}, function(response) {
            //this will only get run if you try to click the button before the page is done loading.
            if (!response){
                console.log("no response.")
                $('#info').html("Loading...")
            }
        });
    });

}

// this function listens for messages from either the background script or the content script (selectimage.js)
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    //this will only get run if you try to click the button before the page is done loading.
    if (request.greeting == "ready"){
        console.log("got ready message")
        $('#info').html("")
        openDialog();
  }
  });

openDialog();