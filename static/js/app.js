$('#loadForm').submit(function(e) {
    var postData = $(this).serializeArray();
    var formURL = $(this).attr("action");

    $.ajax({
        url : formURL,
        type: "POST",
        data : postData,
        success: function(data, textStatus, jqXHR) {
            alert('yes');
        }
    });

});