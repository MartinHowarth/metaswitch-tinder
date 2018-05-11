function result(user_choice) {
  console.log(user_choice);
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


var xDown = null;

function handleDragStart(evt) {
  xDown = evt.clientX;
};

function handleTouchStart(evt) {
  xDown = evt.touches[0].clientX;
};

function handleTouchEnd(evt) {
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
  if ( xDiff > 2 ) result('reject-match');
  if ( xDiff < -2 ) result('accept-match');
  xDown = null;
};