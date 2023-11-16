/*jshint esversion: 6 */
$(document).ready(function() {


    $(".thank-you-container").hide();
  
    // close after press X (close) button
    $(".btn-close").click(function() {
        $(".thank-you-container").hide();
        $("#contact-form").show();
    });

    // Function to show/hide the message based on the selected value
    function updateCategoryMessage() {
        var selectedCategory = $("#category_id").val();
        if (!selectedCategory || selectedCategory === "Choose Category") {
            $("#categoryMessage").show();
            // Disable the form submission
            $("form").attr("onsubmit", "return false;");
        } else {
            $("#categoryMessage").hide();
            // Enable the form submission and update the hidden input field
            $("form").removeAttr("onsubmit");
            $("#selectedCategory").val(selectedCategory);
        }
    }

    // Attach the function to the change event of the dropdown
    $("#category_id").change(updateCategoryMessage);

    // Call the function initially to set the initial state
    updateCategoryMessage();


  });
  
  
  
  
  
    