
    var fileStatuses = {}; // To store file upload statuses
    var requiredFiles = ['aadhar_upload', 'pan_upload', 'selfi_upload', 'income_upload', 'bank_upload', 'esign_upload'];

    function uploadFile(fieldId) {
      var fileInput = document.getElementById(fieldId);
      var file = fileInput.files[0];
      var formData = new FormData();
      formData.append(fieldId, file);

      //file upload status
      var statusElement = document.getElementById(fieldId + '_status');
      statusElement.textContent = 'Uploading...';
      
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/kyc/' + fieldId + "/" + formId, true);
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
          // fileStatuses[fieldId] = xhr.status; // Store the status code for the file upload
          // console.log('File upload status for ' + fieldId + ': ' + xhr.status);
          if (xhr.status === 200) {
            statusElement.textContent = 'Uploaded';
            fileStatuses[fieldId] = xhr.status; // Store the status code for the file upload
            console.log('File upload status for ' + fieldId + ': ' + xhr.status);
          } else {
            statusElement.textContent = 'Error';
            console.log('File upload status for ' + fieldId + ': ' + xhr.status);
          }
          
          checkFormValidity(); // Check form validity after each file upload
        }
      };
      xhr.send(formData);
    }

    function sendData() {
      var form = document.getElementById('el_form');
      var formData = new FormData();

      //spinning
      var submitBtn1 = document.getElementById('submitBtn');
      var spinner = document.getElementById('spinner');
      var formErr = document.getElementById('form-err');
      submitBtn1.style.display = 'none';
      spinner.style.display = 'block';
      
      // Exclude file fields from form data
      var inputElements = form.querySelectorAll('input[type="text"], input[type="date"], input[type="email"], input[type="tel"], input[type="radio"]:checked, select, textarea');
      for (var i = 0; i < inputElements.length; i++) {
        var inputElement = inputElements[i];
        formData.append(inputElement.name, inputElement.value);
      }
      
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/kycform/'+formId, true);
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
          // Hide spinner
          spinner.style.display = 'none';
          
          if (xhr.status === 200) {
            console.log('KYC data submitted successfully!');
            window.location.href = '/';
          } else {
            alert('Error submitting KYC data. Status code: ' + xhr.status);
            submitBtn1.style.display = 'block';
            formErr.style.display = 'block';
          }   
          // Re-enable submit button
          submitBtn.disabled = false;
        }
      };
      xhr.send(formData);
    }
    
    // Add event listeners to check form validity
    var form = document.getElementById('el_form');
    form.addEventListener('change', checkFormValidity);
    
    function checkFormValidity() {
      var isValid = form.checkValidity();
      
      // Check if all required files are uploaded and have 200 status
      var allFilesUploaded = requiredFiles.every(function(fieldId) {
        var status = fileStatuses[fieldId];
        return status === 200;
      });
      
      var submitBtn = document.getElementById('submitBtn');
      submitBtn.disabled = !isValid || !allFilesUploaded;
    }


//Only number
var aadharInput = document.getElementById('aadhar_in');
aadharInput.addEventListener('input', function(event) {
  var inputValue = event.target.value;
  // Remove any non-numeric characters from the input value
  var numericValue = inputValue.replace(/\D/g, '');
  var limitedValue = numericValue.slice(0, 15);
  event.target.value = limitedValue;
});

var pincodeInput = document.getElementById('pincode_in');
pincodeInput.addEventListener('input', function(event) {
  var inputValue = event.target.value;
  // Remove any non-numeric characters from the input value
  var numericValue = inputValue.replace(/\D/g, '');
  var limitedValue = numericValue.slice(0, 9);
  // Update the input field value with the numeric value
  event.target.value = limitedValue;
});


// Get the input field element
var fnameInput = document.getElementById('fname_in');
// Listen for the input event on the text input field
fnameInput.addEventListener('input', function(event) {
  var inputValue = event.target.value;
  // Remove any non-text and non-space characters from the input value
  var sanitizedValue = inputValue.replace(/[^A-Za-z\s]/g, '');
  var limitedValue = sanitizedValue.slice(0, 23);
  event.target.value = limitedValue;
});

// Get the input field element
var snameInput = document.getElementById('sname_in');
// Listen for the input event on the text input field
snameInput.addEventListener('input', function(event) {
  var inputValue = event.target.value;
  // Remove any non-text and non-space characters from the input value
  var sanitizedValue = inputValue.replace(/[^A-Za-z\s]/g, '');
  var limitedValue = sanitizedValue.slice(0, 23);
  event.target.value = limitedValue;
});

// Get the input field element
var guardianInput = document.getElementById('guardian_in');
// Listen for the input event on the text input field
guardianInput.addEventListener('input', function(event) {
  var inputValue = event.target.value;
  // Remove any non-text and non-space characters from the input value
  var sanitizedValue = inputValue.replace(/[^A-Za-z\s]/g, '');
  var limitedValue = sanitizedValue.slice(0, 23);
  event.target.value = limitedValue;
});