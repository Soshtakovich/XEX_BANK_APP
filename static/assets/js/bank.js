document.addEventListener('DOMContentLoaded', () => {
    showContent(null, 'dashboard');

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

        document.querySelectorAll('.nav-button a').forEach(tab => {
            tab.classList.remove('active');
        });

        event.currentTarget.classList.add('active');
    }

    document.querySelectorAll('.tabcontent').forEach(content => {
        content.classList.remove('active');
    });

    const tabContent = document.getElementById(contentId);
    if (tabContent) {
        tabContent.classList.add('active');
    } else {
        console.error(`Tab content with id '${contentId}' not found.`);
    }
}
