console.log('hello world')

const alertBox = document.getElementById('alert-box')
const imageBox = document.getElementById('image-box')
const imageForm = document.getElementById('image-form')
const confirmBtn = document.getElementById('confirm-btn')
const input = document.getElementById('id_product_image')
const input2 = document.getElementById('id_product_image2')
const input3 = document.getElementById('id_product_image3')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

function createCropper(inputElement) {
    inputElement.addEventListener('change', () => {
        alertBox.innerHTML = ""
        confirmBtn.classList.remove('not-visible')
        const img_data = inputElement.files[0]
        const url = URL.createObjectURL(img_data)

        imageBox.innerHTML = `<img src="${url}" id="image" width="700px">`
        var $image = $('#image')

        $image.cropper({
            aspectRatio: 10 /8,
            crop: function(event) {
                console.log(event.detail.x);
                console.log(event.detail.y);
                console.log(event.detail.width);
                console.log(event.detail.height);
                console.log(event.detail.rotate);
                console.log(event.detail.scaleX);
                console.log(event.detail.scaleY);
            }
        });

        var cropper = $image.data('cropper');
        confirmBtn.addEventListener('click', () => {
            cropper.getCroppedCanvas().toBlob((blob) => {
                console.log('confirmed')
                const fd = new FormData();
                fd.append('csrfmiddlewaretoken', csrf[0].value)
                fd.append(inputElement.name, blob, 'my-image.png');

                $.ajax({
                    type: 'POST',
                    url: imageForm.action,
                    enctype: 'multipart/form-data',
                    data: fd,
                    success: function(response) {
                        console.log('success', response)
                        alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                                Successfully saved and cropped the selected image
                                            </div>`
                                            window.location.href = `http://127.0.0.1:8000/products/`;
                    },
                    error: function(error) {
                        console.log('error', error)
                        alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                                Ups...something went wrong
                                            </div>`
                    },
                    cache: false,
                    contentType: false,
                    processData: false,
                })
            })
        })
    });
}

createCropper(input);
createCropper(input2);
createCropper(input3);  

