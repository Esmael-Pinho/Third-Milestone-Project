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
            console.log("Before: Selected Category:", $("#category_id").val());
            var selectedCategory = $("#category_id").val();
            console.log("Selected Category:", selectedCategory);
            if (!selectedCategory || selectedCategory === "Choose Category") {
                $("#categoryMessage").show();
                // Disable the form submission
                $("form").attr("onsubmit", "return false;");
                // Disable the form submission for forms without the "log-reg-cat" class
                $("form:not(.log-reg-cat)").attr("onsubmit", "return false;");
            } else {
                $("#categoryMessage").hide();
                // Enable the form submission and update the hidden input field
                $("form").removeAttr("onsubmit");
                $("form:not(.log-reg-cat)").removeAttr("onsubmit");
                $("#selectedCategory").val(selectedCategory);
            }
            // Attach the function to the change event of the dropdown
            $("#category_id").change(updateCategoryMessage);
        }
        
        // Call the function to set the initial state
        updateCategoryMessage();


    });
  
  
  
  
  
    