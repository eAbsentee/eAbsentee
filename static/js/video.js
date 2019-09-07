closeModal = function() {
  modal.setContent('');
  modal.destroy();
}

// instanciate new modal
var modal = new tingle.modal({
  footer: true,
  closeMethods: ['overlay', 'escape'],
  onClose: closeModal
});

// set content
modal.setContent('<iframe width="100%" height="400" src="https://www.youtube-nocookie.com/embed/usJyXlkl3G4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>');

modal.addFooterBtn('Close', 'tingle-btn tingle-btn--default tingle-btn--pull-right', closeModal);

// show modal after 5 seconds
setTimeout(function() {
  modal.open();
}, 5000);
