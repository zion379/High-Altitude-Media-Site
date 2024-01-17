// get all fields
const client_name_field = document.getElementById('client-name');
const client_email_field = document.getElementById('client-email');
const client_number_field = document.getElementById('client-phone-number');
const project_location_field = document.getElementById('property-location');
const project_info_field = document.getElementById('project-info-text-area');

// get all labels
const client_name_label = document.querySelector('[for="client-name"]');
const client_email_label = document.querySelector('[for="client-email"]');
const client_number_label = document.querySelector('[for="client-phone-number"]');
const project_location_label = document.querySelector('[for="project-info-text-area"]');
const project_info_label = document.querySelector('[for="project-info-text-area"]');

client_name_field.addEventListener('focusout', function() {
    validateText(client_name_field, client_name_label, 3, 30);
});

client_email_field.addEventListener('focusout', function() {
    validateEmail(client_email_field, client_email_label);
});

project_location_field.addEventListener('focusout', function() {
    validateText(project_location_field, project_location_label, 5, 80);
});

project_info_field.addEventListener('focusout', function() {
    validateText(project_info_field, project_info_label, 0, 200);
});

// Phone input
client_number_field.addEventListener('input', function() {
    formatPhoneNumber(this);
});

function formatPhoneNumber(input) {
    // Remove non-digit characters
    let phoneNumber = input.value.replace(/\D/g, '');

    // Apply the desired format
    if (phoneNumber.length == 10) {
        phoneNumber = `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3, 6)}-${phoneNumber.slice(6)}`;
    }

    //Update the input value
    input.value = phoneNumber;
}