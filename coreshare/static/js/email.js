/*jshint esversion: 6 */

// form
const originalFormContent = $("#contact-form").html();
showForm();

function sendEmail(contactForm) {
$("#contact-btn").val("Sending..."); // extra feedback for the user
emailjs.send("gmail", "pinho", {
    "from_email": contactForm.email.value,
    "from_name": contactForm.name.value,
    "message": contactForm.message.value
})
.then(
    function(response) {
        console.log("SUCCESS", response);
        $("#contact-btn").val("Msg Sent"); 
        $("#contact-form").hide();
        $(".thank-you-container").show();
        showThankYou();
    },
    function(error) {
        console.log("FAILED", error);
    }
);
return false;
}

// message to display after Feedback/Message sent
function showThankYou() {
    let thankyouMessage = `
        <h2>YOUR MESSAGE HAS BEEN SENT</h2>
        <br>
        <p>Thank you for the Feedback | Message<br>
        I appreciate your contribution and will be in touch when possible.
        <br>Have a good day! 🤗</p>`;
    $('.thank-you-message').html(thankyouMessage);
}

// Function to show form again after close-btn clicked
function showForm() {
    $(".btn-close").click(function() {
        $("#contact-form").html(originalFormContent);
    });
}
