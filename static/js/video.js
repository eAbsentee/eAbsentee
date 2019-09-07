(function($) {
  // instanciate new modal
  var modal = new tingle.modal({
    // cssClass: ['custom-class-1', 'custom-class-2'],
  });

  modal.addFooterBtn('Close', 'tingle-btn tingle-btn--default tingle-btn--pull-right button', function() {
    modal.close();
  });


  // set content
  modal.setContent('<iframe width="100%" height="400" src="https://www.youtube.com/embed/usJyXlkl3G4?autoplay=1" frameborder="0" allowfullscreen></iframe>');
  // modal.setContent('<iframe width="100%" height="400" src="https://www.youtube-nocookie.com/embed/usJyXlkl3G4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>');

  setTimeout(function() {
    modal.open();
  }, 5000);

})(jQuery);
