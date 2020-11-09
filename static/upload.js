const url = "/";
function bottum() {
	document.getElementById('begin').scrollIntoView({behavior: "smooth"});
};

/* On clicking an image to upload,  replace draggable input box 
 * with the uploaded image in a border*/
function display() {
    document.getElementById('drag-box').style.display = "none"
    document.getElementById('show-image').style.display = "block"
    const files = document.querySelector('[type=file]').files;
    const formData = new FormData();
    var image = document.getElementById('image');
    image.src = URL.createObjectURL(files[0]);
}

/* On clicking GO button, return the response from app.py using fetch */
function uploadImage() {
    document.getElementById('code').innerHTML = 'Loading...';
    const files = document.querySelector('[type=file]').files;
    const formData = new FormData();
    if (files.length == 0) {
        document.getElementById('code').innerHTML = 'Please upload an image first (see step 1)';
        return false;
    }

    for (let i = 0; i < files.length; i++) {
        let file = files[i];
        formData.append('image', file);
    }
    fetch(
        url,
        {
            method: 'POST',
            body: formData,
        }
    ).then((response) => {
        if (response.status == 200) {
            // successful upload
            document.getElementById('error').innerHTML = "";
            return response.text().then((response_text) => {
                document.getElementById('code').innerHTML ="Style: " + response_text;
            });
        } 
        else {
            // unsuccessful upload, displays an error
            document.getElementById('code').innerHTML = "";
            return response.text().then((response_text) => {
                console.log(response_text);
                document.getElementById('error').innerHTML = "Error: " + response_text;
            });
        }
    })
    ;        
    return false;
}
