

let updateBtns = document.getElementsByClassName('update-cart')


for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        let productionId = this.dataset.product
        let action = this.dataset.action

        if (user == 'AnonymousUser') {
            addCookieItem(productionId, action)
        } else {
            updateUserOrder(productionId, action)
        }
    })

}

//add item into cart saved in cookie for guest
function addCookieItem(productId, action){
    console.log("user is not authenticated");

    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {"quantity" : 1}
        }else{
            cart[productId]['quantity'] += 1
        }
    //our cookie object will contain nested objects with the id of the product being the id and the quantity
    }

    if(action == "remove"){
        cart[productId]['quantity'] -= 1
        //check if quantity =0 => remove item from cart
        if(cart[productId]['quantity'] <= 0){
            console.log('Remove item');
            delete cart[productId]
        }
    }

    //rewrite to cookie file after update item
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    console.log(cart);
    location.reload();
}

function updateUserOrder(productId, action) {
    console.log('user is logged in, sending data...');

    let url = '/update_item/'

    // function wait for sending data to server
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken, //this token must have any time call POST method 
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



