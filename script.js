var url = 'http://127.0.0.1:8000/image-decodeText'
var url2 = 'https://jsonplaceholder.typicode.com/posts'
const myHeaders = new Headers();
myHeaders.append('Access-Control-Allow-Headers', "*")
myHeaders.append('Access-Control-Allow-Origin', "*")
// https://nameless-savannah-47105.herokuapp.com/
fetch(url,{
    method: 'GET',
    headers: myHeaders,
}
).then(function (response) {
    // The API call was successful!
    console.log('success!', response);
}).catch(function (err) {
    // There was an error
    console.warn('Something went wrong.', err);
});