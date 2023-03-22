// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-analytics.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyCWBwptep-xQniKao8-vIveXn8EaGlnCoo",
    authDomain: "movie-recommendation-mac-ab36e.firebaseapp.com",
    databaseURL: "https://movie-recommendation-mac-ab36e-default-rtdb.firebaseio.com",
    projectId: "movie-recommendation-mac-ab36e",
    storageBucket: "movie-recommendation-mac-ab36e.appspot.com",
    messagingSenderId: "539183988934",
    appId: "1:539183988934:web:53af7fb4984d40f48ad7c7",
    measurementId: "G-VGNKELDQX5"
};
// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
import { getDatabase, ref, get, set, child }
    from "https://www.gstatic.com/firebasejs/9.18.0/firebase-database.js"
const db = getDatabase();

var username = document.querySelector("#username");
var title = document.querySelector("#title");
var rating = document.querySelector("#rating");
var review = document.querySelector("#review");
var insertBtn = document.querySelector("#insert");
function InsertData() {
    set(ref(db, "Users/" + username.value + "/" + title.value), {
        Username: username.value,
        Title: title.value,
        Review: review.value,
        Rating: rating.value
    })
        .then(() => {
            alert("Data added successfully");
            document.getElementById("myForm").reset();
        })
        .catch((error) => {
            alert(error);
        });
}
insertBtn.addEventListener('click', InsertData);