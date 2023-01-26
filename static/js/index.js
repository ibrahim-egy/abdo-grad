function showImage(event) {

    var image = document.getElementById('img')
    image.src = URL.createObjectURL(event.target.files[0]);

    document.querySelector('.img-box').style.visibility = 'visible'
    document.getElementById('submit-btn').style.visibility = 'visible'
    document.querySelector('.flashes').style.visibility = 'hidden'
}
window.onload = function () {
    preloader.classList.toggle('display')
}

const closeBtn = document.querySelector('.history__close');
const history = document.querySelector('.history');
closeBtn.addEventListener('click', () => {
    history.classList.toggle('close')
    historyLink.classList.toggle('active')
    document.querySelector('.history__close-label').classList.toggle('clicked')
})

const historyLink = document.querySelector('.navigation__link-history');
historyLink.addEventListener('click', (e)=> {
    e.preventDefault();
    historyLink.classList.toggle('active')
    history.classList.toggle('close');
    document.querySelector('.history__close-label').classList.toggle('clicked');
})



const allForms = document.querySelectorAll('form');

if (allForms) {
    allForms.forEach(form => {
        form.onsubmit = function () {
            preloader.classList.toggle('display');
        }
    });
}

const logoutLink = document.querySelector('.logout')


const readLink = document.querySelector('#read-me')
readLink.addEventListener('click', () => {

    document.querySelector("#input").checked = true;
})





