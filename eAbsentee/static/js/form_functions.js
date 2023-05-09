// remap jQuery to $

(function($) {
  /* trigger when page is ready */
  $(document).ready(function() {

    $("input[name=\"permanent_absentee\"]").on("load change", function() {
      if (this.checked) {
        $("#permanent_absentee_div").slideDown();
        $("#one_election_div").slideUp();
        $("#ballot_address").slideUp();
      }
      else {
        $("#permanent_absentee_div").slideUp();
        $("#one_election_div").slideDown();
        $("#ballot_address").slideDown();
      }
    });

    // Hide different delivery address by default
    // Show it if a change is found in where to deliver
    $("#ballot_address_div").hide();
    $("input[name=\"ballot_address_check\"]").change(function() {
      if (this.checked) {
        $("#ballot_address_div").slideDown();
      }
      else {
        $("#ballot_address_div").slideUp();
      }
    });

    $("#assistance_div").hide();
    $("input[name=\"assistance_check\"]").change(function() {
      if (this.checked) {
        $("#assistance_div").slideDown();
      }
      else {
        $("#assistance_div").slideUp();
      }
    });

    $("#change_div").hide();
    $("input[name=\"change_check\"]").change(function() {
      if (this.checked) {
        $("#change_div").slideDown();
      }
      else {
        $("#change_div").slideUp();
      }
    });

    // $("input[name=\"change_check\"]").change(function() {
    //   if (this.checked) {
    //     $("#change_div").slideDown();
    //   }
    //   else {
    //     $("#change_div").slideUp();
    //   }
    // });

    // If an assistant has signed the form, note that in the applicant signature field.
    $("input[name=\"assistant__signed\"]").change(function() {
      if (this.checked) {
        $("input[name=\"signature\"]").val("Applicant Unable to Sign");
      } else {
        $("input[name=\"signature\"]").val("");
      }
    });

    // change state_or_country to state if a state
    $("select[name=\"deliv-state\"]").change(function() {
      var val = $(this).find("option:selected").val();
      $("input[name=\"delivery__state_or_country\"]").val(val);
    });

    // change state_or_country to country if a country other than US,
    // and remove state/ZIP fields
    $("select[name=\"country\"]").change(function() {
      var val = $(this).find("option:selected").val();
      if (val != "United States") {
        $("input[name=\"delivery__state_or_country\"]").val(val);
        $("#delivery__statezip").hide();
      } else {
        $("input[name=\"delivery__state_or_country\"]").val($("select[name=\"deliv - state \"] option:selected").val());
        $("#delivery__statezip").show();
      }
    });

    $(function() {
         $('input[readonly]').on('focus', function(ev) {
               $(this).trigger('blur');
         });
    });

    $(":input").inputmask();

    // disable submit button when pressed, so that multiple requests don't get submitted
    $("#submit_button").click(function() {
      if (document.querySelector('#applicant-form').checkValidity()){
        $(this).prop("disabled", true);
        $(this).html("Submitting...");
      }
    });
  });

})(window.jQuery);
