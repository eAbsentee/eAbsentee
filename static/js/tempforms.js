$(function() {
  let myAuthId = "13682609015195317";

  function getSuggestions(search) {
    // console.log(search);
    $.ajax({
      url: "https://us-autocomplete.api.smartystreets.com/suggest?",
      data: {
        "key": myAuthId,
        "prefix": search,
        "state_filter": "VA"
      },
      dataType: "jsonp",
      success: function(data) {
        if (data.suggestions) {
          buildMenu(data.suggestions);
        } else {
          noSuggestions();
        }
      },
      error: function(error) {
        return error;
      }
    });
  }

  function getSingleAddressData(address) {
    $.ajax({
      url: "https://us-street.api.smartystreets.com/street-address?",
      data: {
        "key": myAuthId,
        "street": address[0],
        "city": address[1],
        "state": address[2]
      },
      dataType: "jsonp",
      success: function(data) {
        console.log(data);
        // $("#address").html(data[0].delivery_line_1);
        $('input[name=address]').val(data[0].delivery_line_1);
        $('input[name=zip]').val(data[0].components.zipcode);
        $('input[name=city]').val(data[0].components.city_name);
      },
      error: function(error) {
        return error;
      }
    });
  }

  // Understood
  function clearAddressData() {
    $("#address").val('');
    $("#zip").val('');
    $("#city").val('');
  }

  // Understood
  function noSuggestions() {
    var menu = $(".us-autocomplete-pro-menu");
    menu.empty();
    menu.append("<li class='ui-state-disabled'><div>No Suggestions Found</div></li>");
    menu.menu("refresh");
  }

  function buildAddress(suggestion) {
    // console.log(suggestion)
    var whiteSpace = "";
    if (suggestion.secondary || suggestion.entries > 1) {
      if (suggestion.entries > 1) {
        suggestion.secondary += " (" + suggestion.entries + " more entries)";
      }
      whiteSpace = " ";
    }
    var address = suggestion.street_line + whiteSpace  + " " + suggestion.city + ", " + suggestion.state;
    var inputAddress = $("#us-autocomplete-pro-address-input").val();
    for (var i = 0; i < address.length; i++) {
      var theLettersMatch = typeof inputAddress[i] == "undefined" || address[i].toLowerCase() !== inputAddress[i].toLowerCase();
      if (theLettersMatch) {
        address = [address.slice(0, i), "<b>", address.slice(i)].join("");
        break;
      }
    }
    return address;
  }

  function buildMenu(suggestions) {
    var menu = $(".us-autocomplete-pro-menu");
    menu.empty();
    suggestions.map(function(suggestion) {
      var caret = (suggestion.entries > 1 ? "<span class=\"ui-menu-icon ui-icon ui-icon-caret-1-e\"></span>" : "");
      menu.append("<li><div data-address='" +
        suggestion.street_line + (suggestion.secondary ? " " + suggestion.secondary : "") + ";" +
        suggestion.city + ";" +
        suggestion.state + "'>" +
        caret +
        buildAddress(suggestion) + "</b></div></li>");
    });
    menu.menu("refresh");
  }

  $(".us-autocomplete-pro-menu").menu({
    select: function(event, ui) {
      var text = ui.item[0].innerText;
      var address = ui.item[0].childNodes[0].dataset.address.split(";");
      var searchForMoreEntriesText = new RegExp(/(?:\ more\ entries\))/);
      if (text.search(searchForMoreEntriesText) == "-1") {
        $("#us-autocomplete-pro-address-input").val(text);
        $(".us-autocomplete-pro-menu").hide();
        getSingleAddressData(address);
      } else {
        $("#us-autocomplete-pro-address-input").val(address[0] + " ");
        address.splice(1, 0, "*");
        address = address.join(" ");
        getSuggestions(address);
      }
    }
  });

  $("#us-autocomplete-pro-address-input").keyup(function(event) {
    var menu = $(".us-autocomplete-pro-menu");
    if ($("#address").val()) clearAddressData();
    if (event.key === "ArrowDown") {
      menu.focus();
      menu.menu("focus", null, menu.menu().find(".ui-menu-item"));
    } else {
      var textInput = $("#us-autocomplete-pro-address-input").val();
      if (textInput) {
        menu.show();
        getSuggestions(textInput);
      } else {
        menu.hide();
      }
    }
  });

});
