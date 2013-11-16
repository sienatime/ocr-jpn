console.log("selectimage.js is a content script")

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    console.log("listening for message")
    if (request.action == "screenshot"){
        console.log(request.data)
    }
    return true;

  });


// function turnBgRed(){
//     document.body.style.background="red"
// }

// function ListeningMethod(request, sender, callback)
// {
//     console.log("listening")
//   if (request.action == 'turnBgRed')
//     turnBgRed();
// }

// chrome.extension.onRequest.addListener(ListeningMethod);