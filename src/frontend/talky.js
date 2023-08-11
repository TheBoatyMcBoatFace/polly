var converter = new showdown.Converter();

$('#question-form').on('submit', function(e) {
    e.preventDefault();
    var question = $('#question-input').val();
    $('#question-input').val('');
    $('#messages').append('<div class="message user-message">You: ' + question + '</div>');
    $('#spinner').show();  // Show spinner
    $.ajax({
        url: '/ask',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({
            'question': question
        }),
        success: function(response) {
            var html = converter.makeHtml(response.response);  // Convert markdown to HTML
            $('#messages').append('<div class="message bot-message">Civic GPT: ' + html + '</div>');
            $('#messages').scrollTop($('#messages')[0].scrollHeight);  // Scroll to bottom
        },
        error: function(response) {
            $('#messages').append('<div class="message bot-message">Error: ' + response.responseJSON.error + '</div>');
        },
        complete: function() {
            $('#spinner').hide();  // Hide spinner
        }
    });
});


$('#reset-button').on('click', function() {
    $('#messages').empty(); // Clear chat history on the page
    $('#messages').append('<div class="message bot-message">Ready to Taco Bout Things...</div>');
    $('#question-input').val('');
    $('#spinner').show();  // Show spinner
    $.ajax({
        url: '/reset',
        type: 'post',
        success: function(response) {
            $('#messages').append('<div class="message bot-message">Chatbot reset successfully</div>');
        },
        error: function(response) {
            $('#messages').append('<div class="message bot-message">Error resetting the chatbot: ' + response.responseJSON.error + '</div>');
        },
        complete: function() {
            $('#spinner').hide();  // Hide spinner
        }
    });
});
