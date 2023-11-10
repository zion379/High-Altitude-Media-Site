// Validate Text Fields Across site

// Validate Text Fields
function validateText(inputField, inputLabel, minLength, maxLength) {
    var inputValue = inputField.value.trim();

    if (inputValue.length < minLength || inputValue.length > maxLength) {
        alert("The Input '"+ inputLabel.textContent + "' must be between " +  minLength + " and " + maxLength + " characters.");
        return false;
    }

    return true;
}

// Create Functions for validating emails, and urls

/* 
    Idea: thinking of creating a function that takes in a group of fields for a form. this group will be passed into the func
    as an array of objects that contain the element and a input type attribute. using the input type to determine how to validate a given input field.
    the benefit of this is it allows for only one alert where multiple alerts would be displayed to the user. 
*/