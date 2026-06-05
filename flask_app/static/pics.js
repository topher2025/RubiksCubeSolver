const MAX_FILES = 3;
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB per file
const ALLOWED_MIME = ['image/jpeg', 'image/png'];
const ALLOWED_EXT = ['.jpg', '.jpeg', '.png'];

function humanFileSize(bytes) {
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file-input');
    const form = document.getElementById('pics-form');
    const errorsEl = document.getElementById('file-errors');
    const submitBtn = document.getElementById('submit-btn');

    function validateFiles(files) {
        const errors = [];
        if (!files || files.length === 0) {
            errors.push('Please select at least one image.');
            return errors;
        }

        if (files.length > MAX_FILES) {
            errors.push(`Maximum ${MAX_FILES} files allowed. You selected ${files.length}.`);
        }

        Array.from(files).forEach(file => {
            // MIME check if available
            if (file.type && !ALLOWED_MIME.includes(file.type)) {
                errors.push(`File "${file.name}" has unsupported type ${file.type}.`);
            }
            // Extension fallback
            const lower = file.name.toLowerCase();
            if (!ALLOWED_EXT.some(ext => lower.endsWith(ext))) {
                errors.push(`File "${file.name}" has unsupported extension.`);
            }
            if (file.size > MAX_FILE_SIZE) {
                errors.push(`File "${file.name}" exceeds ${humanFileSize(MAX_FILE_SIZE)} limit.`);
            }
        });

        return errors;
    }

    function showErrors(list) {
        if (!list || list.length === 0) {
            errorsEl.style.display = 'none';
            errorsEl.textContent = '';
            submitBtn.disabled = false;
            return;
        }
        errorsEl.style.display = '';
        errorsEl.textContent = list.join('\n');
        submitBtn.disabled = true;
    }

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const files = this.files;
            const errors = validateFiles(files);
            if (errors.length > 0) {
                this.value = '';
            }
            showErrors(errors);
        });
    }

    if (form) {
        form.addEventListener('submit', function(e) {
            const files = fileInput.files;
            const errors = validateFiles(files);
            if (errors.length > 0) {
                e.preventDefault();
                showErrors(errors);
            } else {
                // allow normal POST to /pics
                submitBtn.disabled = true;
            }
        });
    }
});
