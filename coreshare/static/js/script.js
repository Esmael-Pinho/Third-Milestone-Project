/*jshint esversion: 6 */
$(document).ready(function() {


    $(".thank-you-container").hide();
  
    // close after press X (close) button
    $(".btn-close").click(function() {
        $(".thank-you-container").hide();
        $("#contact-form").show();
    });

    function updateCategoryMessage() {
        var selectedCategory = $("#category_id").val();
        if (!selectedCategory || selectedCategory === "Choose Category") {
            $("#categoryMessage").show();
            // Disable the form submission for forms without the "log-reg-cat" class
            $("form:not(.log-reg-cat)").attr("onsubmit", "return false;");
        } else {
            $("#categoryMessage").hide();
            // Enable the form submission and update the hidden input field
            $("form:not(.log-reg-cat)").removeAttr("onsubmit");
            $("#selectedCategory").val(selectedCategory);
        }
    }
    
    // Call the function to set the initial state
    updateCategoryMessage();


  });
  
  
  
  
  
    