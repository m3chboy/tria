const getElement = (selector) => {
    const element = document.querySelector(selector)

    if (element) return element
    throw Error(
        `Please double check your class names, there is no ${selector} class`
    )
}

const linka = getElement('.linka')
const linkb = getElement('.linkb')
const navBtnDOMa = getElement('.box1')
const navBtnDOMb = getElement('.box2')
const actPannela = getElement('.pan1')
const actPannelb = getElement('.pan2')
const seeAll = getElement('#see-all')
const bar = getElement('.mobile')
const close = getElement('#close')
const nav = getElement('#navbar')

// Nav
bar.addEventListener('click', () => {
    nav.classList.toggle('active')
})
close.addEventListener('click', () => {
    nav.classList.toggle('active')
})

// Faq
seeAll.addEventListener('click', () => {
    linka.classList.toggle('active')
    actPannela.classList.toggle('active')
    linkb.classList.toggle('active')
    actPannelb.classList.toggle('active')

    var rota = actPannela.nextElementSibling
    rota.classList.toggle('rote')
    var rotb = actPannelb.nextElementSibling
    rotb.classList.toggle('rote')

})

navBtnDOMa.addEventListener('click', () => {
    linka.classList.toggle('active')
    actPannela.classList.toggle('active')

    var rot = actPannela.nextElementSibling
    rot.classList.toggle('rote')
})

navBtnDOMb.addEventListener('click', () => {
    linkb.classList.toggle('active')
    actPannelb.classList.toggle('active')

    var rot = actPannelb.nextElementSibling
    rot.classList.toggle('rote')
})


// ========== click =========

// var acc = document.getElementsByClassName("card");
// var i;


// for (i = 0; i < acc.length; i++) {
//     acc[i].addEventListener("click", function() {

//         this.classList.toggle('card1')
//         var cBody = this.firstElementChild;
//         cBody.classList.toggle('carddis')
//             // console.log(cBody)
//         var cText = cBody.nextElementSibling;
//         cText.classList.toggle('ctest')
//     });
// }



// Calculator

const mPay = getElement('#mpay')
const nPay = getElement('#npay')
const tPay = getElement('#tpay')
const iPay = getElement('#ipay')

function Calculate() {
    let amount = getElement('#principle').value
    let rate = getElement('#rate').value
    let term = getElement('#term').value

    if (term) {
        console.log(term)
    } else {
        console.log(termq)
    }

    if (amount) {
        console.log(term)
    } else {
        console.log(termq)
    }

    if (rate) {
        console.log(term)
    } else {
        console.log(termw)
    }

    // convert rate for 12m to 1m
    const mRate = (rate) / 12 / 100;
    //emi formula
    let emi = ((amount * mRate * (1 + mRate) ** term) / (((1 + mRate) ** term) - 1));
    //total
    let totalAmout = emi.toFixed(2) * term
    let totalInterest = totalAmout.toFixed(2) - amount

    // show monthly pay
    mPay.innerHTML = '₹ ' + emi.toFixed(2)

    //show months
    nPay.innerHTML = term

    //Show total amount
    tPay.innerHTML = '₹ ' + totalAmout.toFixed(2)

    //Show total interest
    iPay.innerHTML = '₹ ' + totalInterest.toFixed(2)

    // if (term) {
    //     nPay.innerHTML = term
    // } else {
    //     nPay.innerHTML = '7'
    // }
}