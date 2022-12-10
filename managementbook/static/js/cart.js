function addToCart(id, name, price) {
    event.preventDefault()
    fetch('/api/cart', {
        method: 'post',
        body: JSON.stringify ({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.JSON()).then(data => {
        console.info(data)
        let d = document.getElementByClassName("cart-counter")
        for(let i=0; i < d.length; i++)
            d[i].innerText = data.total_quantity
    })
    window.location.href = "/cart";
}

function pay() {
    event.preventDefault()

}