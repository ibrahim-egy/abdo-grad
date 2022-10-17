function showImage(event) {

    var image = document.getElementById('img')
    image.src = URL.createObjectURL(event.target.files[0]);

    document.querySelector('.img-box').style.visibility = 'visible'
    document.querySelector('.img-box').style.marginTop = '50px'
    document.getElementById('submit-btn').style.visibility = 'visible'

}