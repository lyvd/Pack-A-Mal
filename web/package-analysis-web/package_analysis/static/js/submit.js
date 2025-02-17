// submit apk file for dashboard

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file');
    const uploaderArea = document.getElementById('dndupload');
    const uploadProgress = document.getElementById('uploadprogress');
    const uploadLabel = document.getElementById('info');
    const textIdle = uploadLabel.querySelector('.text-idle');
    const textDropped = uploadLabel.querySelector('.text-dropped');
    const textDone = uploadLabel.querySelector('.text-done');
    const textError = uploadLabel.querySelector('.text-error');

    fileInput.addEventListener('change', function() {
        if (fileInput.files.length > 0) {
            // Change CSS after file upload
            uploaderArea.style.backgroundColor = '#e0f7fa'; 
            uploaderArea.style.border = '2px solid #00796b'; 
            uploadProgress.style.backgroundColor = '#4caf50';
            uploadProgress.style.height = '20px'; 
            uploadProgress.value = 100; 

            // Change text and visibility
            textIdle.style.display = 'none';
            textDropped.style.display = 'none';
            textDone.style.display = 'block';
            textError.style.display = 'none';

            
        }
    });


});
