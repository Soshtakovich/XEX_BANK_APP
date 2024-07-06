document.addEventListener('DOMContentLoaded', () => {
    // Show Dashboard tab content by default
    showContent(null, 'dashboard');

    // Add event listeners for tab links
    document.querySelectorAll('.nav-button a').forEach(tab => {
        tab.addEventListener('click', (event) => {
            const contentId = tab.getAttribute('data-content-id');
            showContent(event, contentId);
        });
    });
});

function showContent(event, contentId) {
    if (event) {
        event.preventDefault();

        // Remove active class from all tab links
        document.querySelectorAll('.nav-button a').forEach(tab => {
            tab.classList.remove('active');
        });

        // Add active class to the clicked tab link
        event.currentTarget.classList.add('active');
    }

    // Hide all tab contents
    document.querySelectorAll('.tabcontent').forEach(content => {
        content.classList.remove('active');
    });

    // Show the corresponding tab content if found
    const tabContent = document.getElementById(contentId);
    if (tabContent) {
        tabContent.classList.add('active');
    } else {
        console.error(`Tab content with id '${contentId}' not found.`);
    }
}
