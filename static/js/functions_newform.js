// Browser detection for when you get desparate. A measure of last resort.
// http://rog.ie/post/9089341529/html5boilerplatejs

// var b = document.documentElement;
// b.setAttribute("data-useragent",  navigator.userAgent);
// b.setAttribute("data-platform", navigator.platform);

// sample CSS: html[data-useragent*="Chrome/13.0"] { ... }


// remap jQuery to $
(function($) {
  /* trigger when page is ready */
  $(document).ready(function() {

    // Hide different delivery address by default
    // Show it if a change is found in where to deliver
    $("#different_address").hide();
    $("input[name=\"where_deliver\"]").change(function() {
      if ($(this).val() == "diff_address") {
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



    // update locality hidden field with locality_gnis select value
    $("select[name=\"election__locality_gnis\"]").change(function() {
      var val = $(this).find("option:selected").text();
      $("input[name=\"election__locality\"]").val(val);
    });

    // require a reasonable explanation and permit email ballot delivery for some reasons
    $("input[name=\"reason__code\"]").change(function() {

      var label = "";
      var doc_field = $("#reason__documentation");
      doc_field.show();


      if (label !== "") {
        $("label[for=\"reason__documentation_field\"]").text(label);
        $("#reason__documentation_field").prop("required", true);
      }

      // Only show email/fax if 6A-6D selected
      // TODO: instead of completely hiding element, just toggle whether it's required
      $("#delivery_email").hide();
      if ($(this).val() == "6A" || $(this).val() == "6B" || $(this).val() == "6C" || $(this).val() == "6D") {
        $("#delivery_email").show();
      } else {
        $("#delivery_email").hide();
      }
    });

    // Only display the delivery-to address fields if it's necessary
    $("#delivery_address").hide();
    $("input[name=\"delivery__to\"]").change(function() {
      if ($(this).val() == "mailing address") {
        $("#delivery_address").show();
      } else {
        $("#delivery_address").hide();

        // Require an email address, if that's the selected delivery method
        if ($(this).val() == "email") {
          $("#more_info__email_fax").prop("required", true);
        } else {
          $("#more_info__email_fax").prop("required", false);
        }

      }
    });

    // Only display the assistant-info section if it's necessary
    $("#assistant").hide();
    $("input[name=\"assistance__assistance\"]").change(function() {
      if (this.checked) {
        $("#assistant").show();
      } else {
        $("#assistant").hide();
      }
    });

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

    // generate the signature date, which we have to do manually to avoid the inclusion of microseconds
    var d = new Date();
    var formattedDate = d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2) + "T" + ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2) + ":" + ("0" + d.getSeconds()).slice(-2) + "Z";
    $("input[name=\"signature__date\"]").val(formattedDate);

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

  $(window).resize(function() {

  });

})(window.jQuery);
