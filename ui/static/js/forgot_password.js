$("#submit-btn").click((e) => {
    e.preventDefault()
    data = $("form").serialize()
    csrf_token = "{{ csrf_token() }}";

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token)
            }
        }
    });
    $.ajax({
        url: "/user/reset",
        type: "POST",
        data: data,
        dataType: "json",
        success: (res) => {
            $("#password-error").text(res.success)
        },
        error: (err) => {
            $("#password-error").text(err.responseJSON.error)
        }
    })
})