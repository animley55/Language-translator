document.getElementById('image-upload').addEventListener('change', function (event) {
    const preview = document.getElementById('preview-image');
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    } else {
        preview.style.display = 'none';
    }
});

document.getElementById('translate-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = {
        text: document.getElementById('text-to-translate').value,
        source_language: document.getElementById('source-language-select').value,
        target_language: document.getElementById('target-language-select').value
    };

    fetch('/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if(data.translation) {
            document.getElementById('snippet').textContent = data.translation;
        } else {
            alert('Translation failed. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Translation failed. Please try again.');
    });
});
