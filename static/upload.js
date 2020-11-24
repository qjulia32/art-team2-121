const url = "/";

function bottum() {
	document.getElementById('begin').scrollIntoView({behavior: "smooth"});
};

/* On clicking an image to upload,  replace draggable input box 
 * with the uploaded image in a border*/
function display() {
    document.getElementById('drag-box').style.display = "none"
    document.getElementById('show-image').style.display = "block"
    document.getElementById('message').innerHTML = " "
    const files = document.querySelector('[type=file]').files;
    const formData = new FormData();
    var image = document.getElementById('image');
    image.src = URL.createObjectURL(files[0]);
}

function load() {
    document.getElementById('message').innerHTML = 'Loading... (this may take a while)'
}
