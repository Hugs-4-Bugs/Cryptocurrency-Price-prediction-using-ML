$(document).ready(function() {
    // Load the about page content by default
    loadContent('/news/');

    // Handle clicks on navigation links
    $('nav a').click(function(event) {
        event.preventDefault();
        var url = $(this).attr('href');
        loadContent(url);
    });
});

function loadContent(url) {
    $.ajax({
        url: url,
        success: function(data) {
            $('#page-content').html(data);
        }
    });
}
