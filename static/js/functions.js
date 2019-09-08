// Browser detection for when you get desparate. A measure of last resort.
// http://rog.ie/post/9089341529/html5boilerplatejs

// var b = document.documentElement;
// b.setAttribute("data-useragent",  navigator.userAgent);
// b.setAttribute("data-platform", navigator.platform);

// sample CSS: html[data-useragent*="Chrome/13.0"] { ... }


// remap jQuery to $
(function($) {

    // length of an object
    var size = function(obj) {
      var size = 0;
      for (var key in obj) {
        if (obj.hasOwnProperty(key)) size++;
      }
      return size;
    }

    // return an object's first value
    var firstValue = function(obj) {
      for (var key in obj) return obj[key];
    }


    $.fn.serializeObject = function() {

      var o = {};

      $.each(this.find("fieldset"), function() {
        var f = {};
        var fieldset = $(this).attr("id");

        var a = $(this).serializeArray();
        $.each(a, function() {

          // input names follow the format "[fieldset id]_[n]"
          var n = this.name.split("__")[1];

          if (n && this.value !== "") { // ignore the field if it doesn't follow the above format
            if (f[n] !== undefined) {
              if (!f[n].push) {
                f[n] = [f[n]];
              }
              f[n].push(this.value || "");
            } else {
              // make sure booleans aren't expressed as strings
              if (this.value == "true")
                f[n] = true;
              else
                f[n] = this.value || "";
            }
          }
        });

        // add each fieldset object to the meta object
        if (o[fieldset] !== undefined) {
          if (!o[fieldset].push) {
            o[fieldset] = [o[fieldset]];
          }
          o[fieldset].push(f || "");
        } else if (size(f) === 0) { // skip the fieldset if it's blank
          return;
        } else if (size(f) === 1 && fieldset === "assistant") { // don't make a new object for assistant field
          o[fieldset] = firstValue(f) || "";
        } else {
          o[fieldset] = f || "";
        }
      });

      return o;
    };

    /* trigger when page is ready */
    $(document).ready(function() {

        // hide our dialog boxes
        $("#modal-success").modal({
          show: false
        })
        $("#modal-failure").modal({
          show: false
        })

        // hide the email ballot delivery option by default
        $("#delivery_email").hide();

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

          switch ($(this).val()) {
            case "1A":
            case "1B":
              label = "Please enter the name of your college or university.";
              break;
            case "1C":
              label = "Please enter the name of your employer or business";
              break;
            case "6D":
              label = "Please enter the name of your business or employer.";
              $("#delivery_email").show();
              break;
            case "1D":
              label = "Please enter your place of travel (VA county/city or state or country).";
              break;
            case "1E":
              label = "Please enter the name of the employer or business and election day hours of working and commuting (AM to PM).";
              break;
            case "2B":
              label = "Please enter your relationship to the family member.";
              break;
            case "3A":
            case "3B":
              label = "Please enter the name of your institution.";
              break;
            case "6A":
              label = "Please enter your branch of service.";
              $("#delivery_email").show();
              break;
            case "6B":
              label = "Please enter their branch of service.";
              $("#delivery_email").show();
              break;
            case "6C":
              label = "Please enter your last date of residency at your Virginia voting residence only if you have given up that address permanently or have no intent to return.";
              $("#delivery_email").show();
              break;
            case "7A":
              label = "Please enter your new state of residence and date moved from Virginia. Only eligible if you moved less than 30 days before the presidential election.";
              break;
            case "1F":
            case "2A":
            case "2C":
            case "4A":
            case "5A":
            case "8A":
              $("#reason__documentation_field").prop("required", false);
              doc_field.hide();
              break;
          }

          if (label !== "") {
            $("label[for=\"reason__documentation_field\"]").text(label);
            $("#reason__documentation_field").prop("required", true);
          }

          // Only show email/fax if 6A-6D selected
          // TODO: instead of completely hiding element, just toggle whether it's required
          $("#more_info__telephone").hide();
          $("#email").hide();
          if ($(this).val() == "6A" || $(this).val() == "6B" || $(this).val() == "6C" || $(this).val() == "6D") {
            $("#more_info__telephone").show();
            $("#email").show();
          } else {
            $("#more_info__telephone").hide();
            $("#email").hide();
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
            $("input[name=\"signature__signed\"]").val("Applicant Unable to Sign");
          } else {
            $("input[name=\"signature__signed\"]").val("");
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

        // generate the signature date, which we have to do manually to avoid the inclusion of
        // microseconds
        var d = new Date();
        var formattedDate = d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2) + "T" + ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2) + ":" + ("0" + d.getSeconds()).slice(-2) + "Z";
        $("input[name=\"signature__date\"]").val(formattedDate);

      //   $("form").submit(function(e){
      //
      //       e.preventDefault();
      //
      //       // disable the submit button to prevent repeat submissions
      //       $("input:submit").attr("disabled", true);
      //
      //       console.log($("form").serializeObject());
      // }

          // $("form").submit(function(e) {
          //
          //   e.preventDefault();
          //
          //   // disable the submit button to prevent repeat submissions
          //   $("input:submit").attr("disabled", true);
          //
          //   console.log($("form").serializeObject());
          //
          //   $.post(
          //       "https://www.democraticabsentee.com/api/submit/",
          //       JSON.stringify($("form").serializeObject())
          //     )
          //
          //     // on success, display an acknowledgement
          //     .done(function(json, textStatus, ErrorThrown) {
          //
          //       // prohibit resubmissions of the form
          //       $(this).attr("disabled", "disabled");
          //       $(this).parents("form").submit();
          //
          //       // assemble the text of the acknowledgement screen
          //       var response = jQuery.parseJSON(json);
          //       var pdf_url = response.pdf_url;
          //       var registrar_locality = response.registrar.locality;
          //       var registrar_email = response.registrar.email;
          //       var successText = $("#success-message").html();
          //       successText = successText.replace("{{PDF_URL}}", pdf_url);
          //       successText = successText.replace("{{REGISTRAR_LOCALITY}}", registrar_locality);
          //       successText = successText.replace("{{REGISTRAR_EMAIL}}", registrar_email);
          //       $("#success-message").html(successText);
          //
          //       // replace the body content with the success message
          //       $("section").replaceWith($("div#success-message").html());
          //
          //     })
          //
          //     // on failure, display a list of errors
          //     .fail(function(json, textStatus, ErrorThrown) {
          //
          //       // reenable the submit button
          //       $("input:submit").attr("disabled", false);
          //
          //       var response = jQuery.parseJSON(json.responseText);
          //       var errorList = "<ul>";
          //       var errors = response.errors;
          //       $.each(errors, function(type, details) {
          //         errorList = errorList + "<li><strong>" + type + ":</strong> " + details + "</li>";
          //       });
          //       errorList = errorList + "</ul>";
          //
          //       var errorText = $("#failure-message").html();
          //       errorText = errorText.replace("{{ERROR}}", errorList);
          //       $("#failure-message").html(errorText);
          //       $("div#failure-message").toggleClass("hidden");
          //       $("html,body").animate({
          //         scrollTop: $("#failure-message").offset().top
          //       }, "slow");
          //
          //     });
          //
          //   return false;
          // });

        });


      /* optional triggers
  /* optional triggers

 $(window).load(function() {

 });

 $(window).resize(function() {

 });

 */
      $(window).load(function() {
        $("input:submit").attr("enabled", true);
      });
      /* optional triggers

 $(window).load(function() {

 });

 $(window).resize(function() {

 });

 */
      $(window).resize(function() {

      });
      /* optional triggers

 $(window).load(function() {

 });

 $(window).resize(function() {

 });

 */


    })(window.jQuery);
