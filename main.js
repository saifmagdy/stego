const url = 'http://127.0.0.1:8000/image-decodeLeast/'
//var url2 = 'https://jsonplaceholder.typicode.com/posts'
const myHeaders = new Headers();
myHeaders.append('Access-Control-Allow-Headers', "*")
myHeaders.append('Access-Control-Allow-Origin', "*")
myHeaders.append('content-type', 'application/json')

//var data = new FormData();
var base;


const inpFile = document.getElementById("upload")
const previewContainer = document.getElementById("imagePreview")
const previewImage = previewContainer.querySelector(".image-preview-image")
const previewDefaultText = previewContainer.querySelector(".image-preview-default-text")

  
inpFile.addEventListener("change", function(){
  const file = this.files[0]

  if (file) {
    reader = new FileReader();

    previewDefaultText.style.display = "none";
    previewImage.style.display = "block";

    reader.addEventListener("load", function(){
      base = this.result;
      //data.append('img', JSON.stringify(base))
      console.log(base)
      previewImage.setAttribute("src", this.result);
    });

    reader.readAsDataURL(file);

  }else{

    previewDefaultText.style.display = "null";
    previewImage.style.display = "null";
    previewImage.setAttribute("src", "");
  }

});

/* const submitImage = document.getElementById("send");

submitImage.addEventListener("click", fetch(url,{
  method: 'GET',
  headers: myHeaders,
  body: base,
}
).then(function (response) {
  // The API call was successful!
  console.log('success!', response);
}).catch(function (err) {
  // There was an error
  console.warn('Something went wrong.', err);
})); */




//const submitImage = document.getElementById("send");

/* submitImage.addEventListener("Mouse", fetch(url,{
  method: 'POST',
  headers: myHeaders,
  body: data
}
).then(function (response) {
  // The API call was successful!
  console.log('success!', response);
  console.log(data);
}).catch(function (err) {
  // There was an error
  console.warn('Something went wrong.', err);
})); */
function connect(baseImage){
  fetch(url,{
    method: 'POST',
    headers: myHeaders,
    body: baseImage,
  }
  ).then(function (response) {
    // The API call was successful!
    console.log('success!', response);
    console.log(baseImage);
  }).catch(function (err) {
    // There was an error
    console.warn('Something went wrong.', err);
  });
}

function submit(){

  var data = JSON.stringify({ "name": base});
  console.log(data) 
  connect(data);
}



/* var input = document.querySelector('input[type="file"]')
formData.append("file", input.files[0])

fetch(url,{
  method: 'POST',
  headers: myHeaders,
  body: JSON.stringify({
    "img": formData
  }),
}
).then(function (response) {
  // The API call was successful!
  console.log('success!', response);
}).catch(function (err) {
  // There was an error
  console.warn('Something went wrong.', err);
}); */





function hide() {
  var x = document.getElementById("unhiderow");
  var y = document.getElementById("hiderow");
    x.style.display = "none";
    y.style.display = "block";
  }

function unhide() {
  var x = document.getElementById("hiderow");
  var y = document.getElementById("unhiderow");
    x.style.display = "none";
    y.style.display = "block";
}