console.log("selectimage.js is a content script")

// when the page you are on has actually finished loading, selectimage.js sends a message saying it is ready. this way, we can do stuff as soon as the page is done loading.
chrome.runtime.sendMessage({greeting: "ready"}, function(response) {
  console.log(response.farewell);
});

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.greeting == "hello"){

        // if we have "closed" a dialog already, actually get rid of the elements (closing it just sets the display to none but it's hard to get it to come back.)
        if ($('.OCRJPN').css("display") == "none" ){
            $('#OCRJPNdialog').remove()
            $('.OCRJPN').remove()
        }

        // if there is not already an open OCRJPN dialog, add one to the page.
        if( $('.OCRJPN.ui-dialog').length == 0 ){

            d = $('<div id="OCRJPNdialog" title="OCR-JPN"><div id="OCRJPNdialogtext"><button id="OCRJPNocrThis"></button></div><div id="OCRJPNwindowwrapper"><div id="OCRJPNocrwindow"></div></div></div>');

            $('body').append(d);

            // turns dialog HTML into a jQuery UI dialog
            $('#OCRJPNdialog').dialog();

            $('.OCRJPN.ui-dialog').resize(function(){
                // LOL THIS IS WHY I DIDN'T WANT TO DO THIS. sets the height of the OCR window dynamically on resize.
                height = $('#OCRJPNdialog').height() - $('.OCRJPN.ui-dialog #OCRJPNdialogtext').height() - parseInt( $('#OCRJPNwindowwrapper').css('border-bottom') ) - parseInt( $('#OCRJPNwindowwrapper').css('border-top') ) - parseInt( $('#OCRJPNocrwindow').css('border-bottom') ) - parseInt( $('#OCRJPNocrwindow').css('border-top') );
                $('#OCRJPNocrwindow').height(height)
            });
         // capture button
            $( "#OCRJPNocrThis" ).button({ icons: { primary: "ui-icon-check" }});

            // when you click the capture button, send the position of the #ocrwindow. PIL needs 4 coordinates that are x1, y1, x2, y2 and NOT x, y, width, height.
            // important to remember to take into account scrollTop() for when the user has scrolled the page down.
            $('#OCRJPNocrThis').click(function(){
                var x1 = $('#OCRJPNocrwindow').offset().left + parseInt( $('#OCRJPNocrwindow').css('border-left') );
                var y1 = $('#OCRJPNocrwindow').offset().top - $('body').scrollTop() + parseInt( $('#OCRJPNocrwindow').css('border-top') );
                var x2 = $('#OCRJPNocrwindow').offset().left + $('#OCRJPNocrwindow').width();
                var y2 = $('#OCRJPNocrwindow').offset().top + $('#OCRJPNocrwindow').height() - $('body').scrollTop();
                
                // sends a message to background.js to take the screenshot.
                try{
                    chrome.runtime.sendMessage( {greeting: "capture", x1:x1, y1:y1, x2:x2, y2:y2}, function(response) {
                        $('body').append(response);
                    });
                }catch(e){
                    console.log("Lost connection to server.")
                }

                // if there is not a kanjiinfo div open already, add one to the page for the response.
                if ( $('#OCRJPNkanjiinfo').length  == 0 ){
                    info = $('<div id="OCRJPNkanjiinfo" class="OCRJPN"><button class="ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only ui-dialog-titlebar-close" role="button" aria-disabled="false" title="close" id="OCRJPNkanjiinfoclose"><span class="ui-button-icon-primary ui-icon ui-icon-closethick"></span><span class="ui-button-text">close</span></button><div id="OCRJPNresultwrapper"><div id="OCRJPNtext"></div><div id="OCRJPNdictwrapper"></div></div></div>');
                    $('body').append(info)
                    // the cancel lets you select the text that appears in the info div.
                    $( "#OCRJPNkanjiinfo" ).draggable({ cancel: "#OCRJPNtext" }); 
                    // there's a close button on the info div.
                    $('#OCRJPNkanjiinfoclose').click(function(){
                        $(this).parent().remove()
                    });
                    $('#OCRJPNkanjiinfo').mouseleave(function(){
                        $('.candidateWrapper').css('display','none');
                    })

                }

                // aligns the info div to the ocr dialog.
                adjustInfoPane();
                loader = chrome.extension.getURL("images/henoheno.gif")
                $('#OCRJPNresultwrapper').html($("<div id='OCRJPNtext'><img src='" + loader + "'></div><div id=\"OCRJPNdictwrapper\"></div>"));
                $('.OCRJPNresult').remove()

            });

            

            // not using this right now but it goes with the code at the bottom of the file.
            $('#OCRJPNtest').click(function(){
                takeScreenshot($('#OCRJPNocrwindow'), renderPreview)
            });

        }
    }else if(request.greeting == "displayResults"){
        // this is what actually adds the results of the AJAX query to the info div.
        // don't parse the JSON--$.ajax did it for you
        if( request.results.candidates.length > 0 ){
            $('#OCRJPNtext').html("");
            $('.candidateWrapper').remove();
            var candidates = request.results.candidates
            console.log(candidates)

            for (var i = 0; i < candidates.length; i++) {
                var characters = candidates[i]
                // maybe make a span or something that has an ID and then put the 0 element in that span
                // then you can do stuff with the other things.
                var id = "chara" + i
                var chara = $('<span id="' + id + '" class="OCRJPNresult"></span>')
                
                var candidate_wrapper = $('<div id="candidateWrapper'+ i + '" class="candidateWrapper"></div>')

                for (var j = 1; j < characters.length; j++) {
                    var candSpan = $('<span id="'+ id + 'candidate'+ j + '" class="OCRJPNcandidate"></span>')
                    candSpan.text(characters[j])
                    candSpan.click(swapChars)
                    candidate_wrapper.append(candSpan)
                };

                chara.text(candidates[i][0])
                
                chara.click(function(){
                    $('.candidateWrapper').css('display','none')
                    id = this.id[5] //ugh this is so bad
                    $('#candidateWrapper'+id).css('display', 'block')
                })
                    $('#OCRJPNtext').append(chara);
                    $('#OCRJPNkanjiinfo').append(candidate_wrapper);
                candidate_wrapper.css('left', $('#' + id).width() * i)
            }
            $("#OCRJPNresultwrapper").append($("<button id='OCRJPNdictionary'>Dictionary</button>"));

            $('#OCRJPNdictionary').click(function(){
                var lookup = $('.OCRJPNresult').text()
                chrome.runtime.sendMessage( {greeting: "dictionary", lookup:lookup}, function(response) {
                    $('#OCRJPNresultwrapper').append(response);
                });
            });
        }else{
            $('#OCRJPNtext').html($("<div class=\"OCRJPNmessage\">Didn't find anything. Resize box and try again.</div>"));
        }
    }else if (request.greeting == "gotDefinition"){
        $('#OCRJPNdictwrapper').html("");
        console.log(request.results)
        results = JSON.parse(request.results)
        
        if (results.length > 0){
            
            for (i = 0; i < results.length; i++){
                var entry = results[i].entry;
                console.log(entry)
                var kanji = entry.kanji
                var readings = entry.readings
                var nihongo = $('<div class="OCRJPNdictkanji">'+kanji+'</div><div class="OCRJPNreadings">'+readings+'</div>')

                $('#OCRJPNdictwrapper').append(nihongo)

                var def_ol = $('<ol class="OCRJPNdeflist"></ol>')
                    for (j = 0; j < entry.senses.length; j++){
                        var english_list = entry.senses[j].glosses.en;
                        def_ol.append($('<li>'+english_list.join(", ")+'</li>'));
                    }
                $('#OCRJPNdictwrapper').append(def_ol)
            }

        }else{
            $('#OCRJPNdictwrapper').html($('<div class="OCRJPNmessage">Didn\'t find anything in the dictionary.</div>'));
        }
        
    }
        
  });

swapChars = function(){
    id = this.id[5]
    swap = $('#chara'+id).text()
    $('#chara'+id).text(this.innerHTML)
    this.innerHTML = swap
}

// for debug purposes only
function printCoords(){
    console.log($('#OCRJPNocrwindow').offset().left)
    console.log($('#OCRJPNocrwindow').offset().top - $('body').scrollTop() - $('body').css('margin-top'))
    console.log($('#OCRJPNocrwindow').offset().left + $('#OCRJPNocrwindow').width())
    console.log($('#OCRJPNdialog').offset().top + $('#OCRJPNdialog').height() + parseInt($('#OCRJPNdialog').css('border-bottom').charAt(0)) - $('body').scrollTop())
}

// aligns the kanji info div with the ocr dialog
function adjustInfoPane(){
    put_top = $('.OCRJPN.ui-dialog').offset().top + 'px'
    put_left = $('.OCRJPN.ui-dialog').offset().left + $('.OCRJPN.ui-dialog').width() + 20 + 'px'

    $('#OCRJPNkanjiinfo').css('top', put_top);
    $('#OCRJPNkanjiinfo').css('left', put_left);
}

// this code is adapted from http://louisrli.github.io/blog/2013/01/16/javascript-canvas-screenshot/#.Uo-pbsR018E. I am not actually using it though. But I kept it just in case.
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