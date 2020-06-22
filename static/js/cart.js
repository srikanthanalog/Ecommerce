var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)
        updateUserOrder(productId, action)
    })
}

function updateUserOrder(productId, action) {
    console.log("User Logged In, Sending Data.....")

    // Send data to backed through api
    // without adding CSRF Token You Can't Send Data To Backed
    var url = '/update_item/'
    fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/Json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ 'productId': productId, 'action': action })
        })
        // response to json
        .then((response) => {
            return response.json()
        })
        // print backed response on console
        .then((data) => {
            console.log("data:", data)
                // reaload page
            location.reload()
        })
}