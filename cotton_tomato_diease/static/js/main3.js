$(document).ready(function () {
    // Init
    $('.image-section1').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            print("js-3")
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview1').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview1').hide();
                $('#imagePreview1').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload1").change(function () {
        print("js-2")
        $('.image-section1').show();
        $('#btn-predict1').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict1').click(function () {
        var form_data = new FormData($('#upload-file1')[0]);
        print("js-1")

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict1',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text(' Result:  ' + data);
                console.log('Success!');
            },
        });
    });

});
