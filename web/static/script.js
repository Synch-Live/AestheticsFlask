/* Use the onended event for the media resource to display hidden slider
   https://html.spec.whatwg.org/multipage/media.html#event-media-ended
*/

document.getElementById('video')
        .addEventListener('ended', function() {
            slid = document.getElementById('slider');
            slid.style.display = 'block';
        }, false);
