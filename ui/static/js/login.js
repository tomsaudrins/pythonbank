$("#submit-btn").click((e) => {
    e.preventDefault()
    console.log("1")
    data = $("form").serialize()
    console.log("2")
    csrf_token = "{{ csrf_token() }}";

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token)
            }
        }
    });
    console.log("3")
    $.ajax({
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: (res) => {
            if (res.changePassword) {
                window.location.href = "/user/changepassword"
            } else {
                window.location.href = "/dashboard"
            }
        },
        error: (err) => {
            console.log(err)
            $("#password-error").text(err.responseJSON.error)
        }
    })
})