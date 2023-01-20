

function showImage(event) {

    var image = document.getElementById('img')
    image.src = URL.createObjectURL(event.target.files[0]);

    document.querySelector('.img-box').style.visibility = 'visible'
    document.getElementById('submit-btn').style.visibility = 'visible'
    document.querySelector('.flashes').style.visibility = 'hidden'
}

window.onload = function () {
    preloader.classList.toggle('display')
    history.classList.toggle('close')
}

const allForms = document.querySelectorAll('form');

if (allForms) {
    allForms.forEach(form => {
        form.onsubmit = function () {
            preloader.classList.toggle('display');
        }
    });
}


const closeBtn = document.querySelector('.history__close');
const history = document.querySelector('.history');
closeBtn.addEventListener('click', () => {
    history.classList.toggle('close')
    historyLink.classList.toggle('active')
    document.querySelector('.history__close-label').classList.toggle('clicked')
})

const historyLink = document.querySelectorAll('.navigation__item')[3];
//const links = document.querySelectorAll('.navigation__link')
historyLink.addEventListener('click', (e)=> {
    e.preventDefault();
    historyLink.classList.toggle('active')
    history.classList.toggle('close');
    document.querySelector('.history__close-label').classList.toggle('clicked');
})