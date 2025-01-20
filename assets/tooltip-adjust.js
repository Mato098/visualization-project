document.addEventListener('DOMContentLoaded', function() {
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'aria-valuenow') {
                const handle = mutation.target;
                const tooltip = handle.nextElementSibling.querySelector('.rc-slider-tooltip-inner');
                if (tooltip) {
                    const value = parseInt(handle.getAttribute('aria-valuenow'), 10) + 1;
                    tooltip.textContent = value;
                }
            }
        });
    });

    const handles = document.querySelectorAll('.rc-slider-handle');
    handles.forEach(function(handle) {
        observer.observe(handle, { attributes: true });
        const tooltip = handle.nextElementSibling.querySelector('.rc-slider-tooltip-inner');
        if (tooltip) {
            const value = parseInt(handle.getAttribute('aria-valuenow'), 10) + 1;
            tooltip.textContent = value;
        }
    });
});