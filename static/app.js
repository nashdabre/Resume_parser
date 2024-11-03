document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();

    // Display loading spinner
    document.getElementById('loading').style.display = 'block';
    document.getElementById('result').style.display = 'none';

    // Get the form data
    let formData = new FormData();
    formData.append('resume', document.getElementById('resume').files[0]);
    formData.append('job_description', document.getElementById('job_description').files[0]);

    // Send data to the Flask API
    fetch('/ats_score', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading spinner
        document.getElementById('loading').style.display = 'none';

        // Display ATS score
        document.getElementById('atsScore').innerText = data.ats_score;
        document.getElementById('result').style.display = 'block';
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        alert('Error occurred. Please try again.');
    });
});