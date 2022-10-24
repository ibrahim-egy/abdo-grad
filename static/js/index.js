//var image = document.getElementById('img')
//image.src = URL.createObjectURL(event.target.files[0]);

function showImage(event) {

    var image = document.getElementById('img')
    image.src = URL.createObjectURL(event.target.files[0]);

    document.querySelector('.img-box').style.visibility = 'visible'
    document.getElementById('submit-btn').style.visibility = 'visible'
    document.querySelector('.flashes').style.visibility = 'hidden'
}



let preloader = document.getElementById("preloader");
preloader.classList.add('display')

window.onload = function () {
    preloader.classList.remove('display')
}

const allForms = document.querySelectorAll('form');

if (allForms) {
    allForms.forEach(form => {
        form.onsubmit = function () {
            preloader.classList.add('display');
        }
    });
}

