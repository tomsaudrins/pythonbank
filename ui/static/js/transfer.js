$("#send-btn").click((e) => {
    e.preventDefault()
    if (!$("#email")[0].value) {
        $("#transfer-error").text("Please enter user's email address!")
        return
    }
    if (!$("#amount")[0].value) {
        $("#transfer-error").text("Please provide an amount!")
        return
    }
    data = $("form").serialize()

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token() }}")
            }
        }
    });
    $.ajax({
        url: "/transfers/send",
        type: "POST",
        data: data,
        dataType: "json",
        success: (res) => {
            $("#transfer-error").text(res.success).addClass("text-green-300").removeClass("invisible")
            $("#amount-span").text(res.new_balance)
            $("#email")[0].value = $("#amount")[0].value = ""
            $("tbody")[0].prepend($("tbody")[0].childElementCount < 5 ? $("tbody")[0].firstElementChild.cloneNode(true) : $("tbody")[0].lastElementChild)
            $(".transaction-type")[0].innerText = res.transaction.type
            $(".transaction-sender")[0].innerText = res.transaction.sender
            $(".transaction-receiver")[0].innerText = res.transaction.receiver
            $(".transaction-id")[0].href = "http://localhost:5000/transactions/" + res.id
            $(".transaction-amount")[0].innerText = "DKK -" + parseFloat(res.transaction.amount).toFixed(2)
            $(".transaction-amount").first().removeClass("text-green-300").addClass("text-red-300")
            $(".transaction-date")[0].innerText = res.transaction.date
            $("#expenses")[0].innerText = parseFloat($("#expenses")[0].innerText) + res.transaction.amount
        },
        error: (err) => {
            $("#transfer-error").removeClass("invisible").text(err.responseJSON.error)
        }
    })
})