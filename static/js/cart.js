let updateBtns = document.getElementsByClassName('update-cart')


for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        let productionId = this.dataset.product
        let action = this.dataset.action

        console.log(productionId, action);
        console.log(user);


        if (user == 'AnonymousUser') {
            console.log("User are not authenticated");
        } else {
            updateUserOder(productionId, action)
        }
    })

}

function updateUserOder(productId, action) {
    console.log('user is logged in, sending data...');

    let url = '/update_item/'

    // function wait for sending data to server
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'productId': productId,
                'action': action
            })
        })
        //wait response from fetch call
        .then((response) => {
            return response.json()
        })

        .then((data) => {
            // console.log('Data : ', data);
            location.reload()
        })
}