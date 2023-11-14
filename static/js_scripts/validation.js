// Validate Text Fields Across site

// Validate Text Fields, returns true if text is valid
function validateText(inputField, inputLabel, minLength, maxLength) {
    var inputValue = inputField.value.trim();

    if (inputValue.length < minLength ) {
        alert("The Input '"+ inputLabel.textContent + "' must be at leeast " +  minLength + " characters.");
        return false;
    } else if (inputValue.length > maxLength) {
        alert("The Input '" + inputLabel.textContent + "' can only be equal to or less than " + maxLength + " charcters. current values is " +  (inputField.value.length - maxLength)  + " chacters over limit.");
        return false;
    }

    return true;
}

// regex expression for checking email formats = /^[^\s@]+@[^\s@]+\.[^\s@]+$/s
// Create Functions for validating emails, and urls

// Returns True if email is valid
function validateEmail(inputField, inputLabel) {
    var inputValue = inputField.value.trim();

    var emailRegex = /[^\s]+@[^\s]+\.[^\s]+/g;

    // Check if the email matches the regular expression
    if (emailRegex.test(inputValue)) {
        console.log('The Field in correct format.');
        return true;
    }
    else {
        alert('The Field ' + inputLabel.textContent + ' is not the correct format. the value needs to be a valid email.');
        return false;
    }
}

function validateURL() {
    // Come back to this
}

function validatePhone(inputField, inputLabel) {

}

// Returns false if no value was selected.
function validateSelection(inputField, inputLabel) {
    // the default selection option value will be set to 'none'
    if(inputField.value == 'none') {
        alert('Please make a selection for the field ' + inputLabel.textContent  + '. currently no value is selected.');
        return false;
    }
    else {
        return true;
    }
}

/* 
    Validate Form Object
    {
        input_element:,
        input_type:

    }
*/

// Constructor function
function Input_field_obj(input_element, label_element, input_type, min_length, max_length) {
    this.input_element = input_element;
    this.label_element = label_element;
    this.input_type = input_type;
    this.min_length = min_length;
    this.max_length = max_length;
}

// returns true if all input fields are valid
function validateForm(form_feilds) {
    // this function takes an array of objects as input
    // loop through array
    // read input_type value to handle validation
    // if validation fails append an error message of elements that have issues
    // display validation message to user.
    var is_form_valid = new Array
    var is_field_valid = new Boolean;

    for(const input_feild of form_feilds) {
        if(input_feild.input_type == 'text') {
            console.log('Validating text');
            is_field_valid = validateText(input_feild.input_element, input_feild.label_element, input_feild.min_length, input_feild.max_length);
        }
        if(input_feild.input_type == 'email') {
            console.log('Validating email');
            is_field_valid = validateEmail(input_feild.input_element, input_feild.label_element);
        }
        if(input_feild.input_type == 'select') {
            console.log('Validating selection');
            is_field_valid = validateSelection(input_feild.input_element, input_feild.label_element);
        }
        if(input_feild.input_type == '') {
            console.log('Input validation field type not set.')
        }
        is_form_valid.push(is_field_valid);
    }

    // check if validation failed.
    for (const is_input_valid of is_form_valid){
        console.log('is input valid : ' + is_input_valid);
        if(is_input_valid == false) {
            return false;
        }
    }

    return true;
}

/* 
    Idea: thinking of creating a function that takes in a group of fields for a form. this group will be passed into the func
    as an array of objects that contain the element and a input type attribute. using the input type to determine how to validate a given input field.
    the benefit of this is it allows for only one alert where multiple alerts would be displayed to the user. 
*/