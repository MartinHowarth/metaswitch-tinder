function result(user_choice) {
  //console.log(user_choice);
  var image = document.getElementById('match-img');
  if (!image) {
    console.log("No image element in page.");
    return;
  }
  // Load a new image but report result.
  document.getElementById(user_choice).click()
}
// On click and drag
document.addEventListener('dragstart', handleDragStart, false);
document.addEventListener('drop', handleDragEnd, false);
document.addEventListener('dragover', handleDragOver, false);

// On mobile swipe action
document.addEventListener('touchstart', handleTouchStart, false);
document.addEventListener('touchmove', handleTouchEnd, false);
window.addEventListener('touchstart', handleTouchStart, false);
window.addEventListener('touchmove', handleTouchEnd, false);


var xDown = null;

function handleDragStart(evt) {
  xDown = evt.clientX;
  swipe_gif = "https://preview.ibb.co/eLrFdy/swipe.gif";
  setDragGhost(swipe_gif, evt);
  }

function setDragGhost(url, evt) {
var img = document.createElement("img");
img.src = url
evt.dataTransfer.setDragImage(img, 220, 20);
}

function handleTouchStart(evt) {
  //evt.preventDefault();
  xDown = evt.touches[0].clientX;
};

function handleTouchEnd(evt) {
  //evt.preventDefault();
  handleEnd(evt.touches[0].clientX);
}

function handleDragOver(evt) {
  evt.preventDefault();
}

function handleDragEnd(evt) {
  evt.preventDefault();
  handleEnd(evt.clientX);
}

function handleEnd(xUp) {
  if ( !xDown ) { return; }
  var xDiff = xDown - xUp;
  if ( xDiff > 100 ) result('reject-match');
  if ( xDiff < -100 ) result('accept-match');
  xDown = null;
};