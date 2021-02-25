// remap jQuery to $

(function($) {
  /* trigger when page is ready */
  $(document).ready(function() {

    $("#all_elections_div").hide();
    $("input[name=\"all_elections\"]").change(function() {
      if ($('input[name="all_elections"]:checked').length > 0) {
        $("#all_elections_div").slideDown();
      }
      else {
        $("#all_elections_div").slideUp();
      }
    });

    // Hide different delivery address by default
    // Show it if a change is found in where to deliver
    $("#different_address").hide();
    $("input[name=\"where_deliver\"]").change(function() {
      if ($('input[name="where_deliver"]:checked').length > 0) {
        $("#different_address").slideDown();
      }
      else {
        $("#different_address").slideUp();
      }
    });

    $("#assistance_div").hide();
    $("input[name=\"assistance_check\"]").change(function() {
      if ($('input[name="assistance_check"]:checked').length > 0) {
        $("#assistance_div").slideDown();
      }
      else {
        $("#assistance_div").slideUp();
      }
    });

    $("#change_div").hide();
    $("input[name=\"change_check\"]").change(function() {
      if ($('input[name="change_check"]:checked').length > 0) {
        $("#change_div").slideDown();
      }
      else {
        $("#change_div").slideUp();
      }
    });

    $("#address_div").hide();
    // $("input[name=\"change_check\"]").change(function() {
    //   if ($('input[name="change_check"]:checked').length > 0) {
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

    $("form").submit(function(e) {
      $("input:submit").attr("disabled", true);
    });

    $(function() {
         $('input[readonly]').on('focus', function(ev) {
               $(this).trigger('blur');
         });
    });

  });

  $(window).load(function() {
    $("input:submit").attr("enabled", true);
  });

})(window.jQuery);
