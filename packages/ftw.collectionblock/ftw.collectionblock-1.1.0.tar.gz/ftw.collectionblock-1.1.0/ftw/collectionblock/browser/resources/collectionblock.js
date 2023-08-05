(function() {

  "use strict";

  $(function() {
    $(document).on("onLoad", ".overlay", function() {
      $.querywidget.initialized = false;
      $.querywidget.init();

      // We need two keep two fields for each sorting field ('#sort_on',
      // '#sort_reversed'). The query results preview that calls
      // '@@querybuilder_html_results' in plone.app.querystring expects a
      // sort_on and sort_order param. To store the actual setting on the
      // collection we need the two z3c.form-based fields
      // ('#form-widgets-ICollection-sort_on', '#form-widgets-ICollection-sort_reversed')

      // Synchronize the '#sort_on' field with the hidden
      // #form-widgets-ICollection-sort_on z3c.form field on load.
      $('#sort_on').val($('#form-widgets-ICollection-sort_on').val());

      // Synchronize the '#sort_order' field with the hidden
      // #form-widgets-ICollection-sort_reversed z3c.form field on load.
      if ($('#form-widgets-ICollection-sort_reversed-0').attr('checked')) {
          $('#sort_order').attr('checked', true);
      } else {
          $('#sort_order').attr('checked', false);
      }

      // Synchronize the z3c.form '#form-widgets-ICollection-sort_on' field
      // with the '#sort_on' field on user interaction
      $("div.QueryWidget").on('change', '#sort_on', function () {
          $('#form-widgets-ICollection-sort_on').val($(this).val());
      });

      // Synchronize the z3c.form '#form-widgets-ICollection-sort_reversed' field
      // with the '#sort_order' field on user interaction.
      $("div.QueryWidget").on('click', '#sort_order', function () {
          if ($(this).is(":checked")) {
              $('#form-widgets-ICollection-sort_reversed-0').attr('checked', true);
          } else {
              $('#form-widgets-ICollection-sort_reversed-0').attr('checked', false);
          }
      });

      // Hide the z3c.form widgets for sorting because they are only needed
      // internally.
      $('#formfield-form-widgets-ICollection-sort_on').hide();
      $('#formfield-form-widgets-ICollection-sort_reversed').hide();

    });
  });
})();
