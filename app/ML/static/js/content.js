const headings = document.querySelectorAll('.heading');
let firstRun = true;

window.addEventListener('scroll', () => {
    const scrollValue = window.scrollY;

    headings.forEach((heading, index) => {
        heading.style.top = `${scrollValue * .07 * index}px`;
        if (firstRun) {
            heading.style.transform = `translateY(0px)`;
        }
    });

    firstRun = false;
});
setTimeout(function () {
    headings.forEach((heading, index) => {
        heading.style.transform = `translateY(${index * 4}px)`;
    });
}, 500);


$(document).on('touchstart', '.modal', function(event) {
    event.stopPropagation();
    var startX = event.changedTouches[0].pageX;
    $(this).one('touchmove', function(event) {
        event.preventDefault();
        var moveX = event.changedTouches[0].pageX;
        if (Math.abs(moveX - startX) > 10) {
            $(this).off('touchmove');
        }
    });
});



$(window).scroll(function () {
    var scrollPosition = $(window).scrollTop();
    var contentSectionPosition = $('.nav-begin').position().top;

    if (scrollPosition > contentSectionPosition) {
        $('nav').addClass('slide-in');
    } else {
        $('nav').removeClass('slide-in');
    }
});



// setTimeout(function(){	
// 	headings.forEach((heading, index) => {
// 		heading.style.transform = `translateY(${index * 4}px)`;
// 	});
// }, 500);

// // get the #landing header element
// const landingHeader = document.getElementById('landing');
// window.addEventListener('scroll', function() {
//   const distanceFromTop = landingHeader.getBoundingClientRect().top;
//   if (distanceFromTop <= 0) {
//   } else {
//     document.querySelector('nav').classList.remove('nav-transparent');
//   }
// });




$(document).ready(function () {
    var contentSection = $('.content-section');
    var navigation = $('nav');

    //when a nav link is clicked, smooth scroll to the section
    navigation.on('click', 'a', function (event) {
        event.preventDefault(); //prevents previous event
        smoothScroll($(this.hash));
    });

    //update navigation on scroll...
    $(window).on('scroll', function () {
        updateNavigation();
    })
    //...and when the page starts
    updateNavigation();

    /////FUNCTIONS
    function updateNavigation() {
        contentSection.each(function () {
            var sectionName = $(this).attr('id');
            var navigationMatch = $('nav a[href="#' + sectionName + '"]');
            if (($(this).offset().top - $(window).height() / 2 < $(window).scrollTop()) &&
                ($(this).offset().top + $(this).height() - $(window).height() / 2 > $(window).scrollTop())) {
                navigationMatch.addClass('active-section');
            }
            else {
                navigationMatch.removeClass('active-section');
            }
        });
    }
    function smoothScroll(target) {
        $('body,html').animate({
            scrollTop: target.offset().top
        }, 800);
    }
});




let reviews = {};
function updateReviewsContainer() {
    let html = "";
    for (let key in reviews) {
        html += `<p><b>Movie:</b> ${reviews[key].Title}, <b>Rating:</b> ${reviews[key].Rating}, <b>Review:</b> ${reviews[key].Review}</p>`;
    }
    $("#reviewContainer").html(html);
}

async function getMoviesInfo(movies) {
    const apiKey = 'b1b26ef2';
    const movieInfoList = [];
    for (const movie of movies) {
        const url = `http://www.omdbapi.com/?t=${movie}&apikey=${apiKey}`;
        const response = await fetch(url);
        if (!response.ok) {
            console.log(`Failed to retrieve data for ${movie}: ${response.statusText}`);
            continue;
        }
        const data = await response.json();

        if (data.Response === 'False') {
            console.log(`Failed to retrieve data for ${movie}: ${data.Error}`);
            continue;
        }
        const movieInfo = {
            title: data.Title,
            poster: data.Poster,
            year: data.Year,
            rating: data.imdbRating,
            genre: data.Genre,
            imdbLink: `https://www.imdb.com/title/${data.imdbID}`
        };

        movieInfoList.push(movieInfo);
    }
    return movieInfoList;
}

function createMovieCards(movieData) {
    const modalBody = $(".carousel_container");
    modalBody.empty();
    const carousel = $("<div class='carousel_Collection'></div>");
    modalBody.append(carousel);

    for (let i = 0; i < movieData.length; i++) {
        const movie = movieData[i];
        const movieCard = $(`<div class="item">
        <div class="card">
        <img class="card-img-top" src="${movie.poster}" alt="${movie.title} poster" style="border-radius: 0px 0px 0 0; width:100%; height:auto;">
        <div class="card-body">
                              <h5 class="card-title">${movie.title}</h5>
                              <h5 class="card-title">${movie.year}</h5>
                              <h5 class="card-title">${movie.genre}</h5>
                              <h5 class="card-title">${movie.rating}</h5>
                            </div>
                            </div>
      </div>`);
        movieCard.on("click", function () {
            window.open(movie.imdbLink, "_blank");
        });
        carousel.append(movieCard);
    }
}
// function createMovieCards(movieData) {
//     const modalBody = $(".modal-body");
//     modalBody.empty();
//     const row = $("<div class='row'></div>");
//     modalBody.append(row);

//     for (let i = 0; i < movieData.length; i++) {
//         const movie = movieData[i];
//         const movieCard = $(`<div class="card mx-2 mb-3 col-md-4" style="width: 18rem; border-radius: 15px; overflow: hidden; cursor: pointer;">
//                             <img class="card-img-top" src="${movie.poster}" alt="${movie.title} poster" style="border-radius: 15px 15px 0 0; width:100%; height:auto;">
//                             <div class="card-body">
//                               <h5 class="card-title">${movie.title}</h5>
//                               <p class="card-text">${movie.year} | ${movie.genre} | IMDB: ${movie.rating}</p>
//                             </div>
//                           </div>`);
//         movieCard.on("click", function () {
//             window.open(movie.imdbLink, "_blank");
//         });
//         row.append(movieCard);
//     }
// }

const modal = `
  <div class="modal fade" id="movieModal" tabindex="-1" aria-labelledby="movieModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-scrollable">
      <div class="modal-content">
      <div class="modal-header">
      <h3 class="modal-title" id="movieModalLabel">Your Personalized Movie Recommendations: </h5>
    </div>
        <div class="modal-body">
            <div class="carousel_container">


            </div>
        </div>
      </div>
    </div>
  </div>
`;
$("body").append(modal);




$("#insert").click(() => {
    const username = $("#username").val();
    const title = $("#title").val();
    const rating = $("#rating").val();
    const review = $("#review").val();

    if (!username || !title || !rating || !review) {
        alert("Please fill in all fields");
        return;
    }
    const key = Date.now().toString();
    reviews[key] = { Username: username, Title: title, Rating: rating, Review: review };
    $("#title").val("");
    $("#rating").val("-");
    $("#review").val("");
    updateReviewsContainer();
});

$("#Done").click(() => {
    if (Object.keys(reviews).length < 2) {
        alert("Please Insert At Least 2 Movie Reviews");
        return;
    }

    // Send reviews to Flask app and get positive, negative, and neutral review counts
    $.ajax({
        type: "POST",
        url: "/recommend",
        data: JSON.stringify({ reviews: reviews }),
        contentType: "application/json",
        success: function (data) {
            getMoviesInfo(data).then((movieData) => {
                createMovieCards(movieData);
                $("#movieModal").modal("show");
            });
        },
        error: function (xhr, status, error) {
            alert("Error: " + error);
        }
    });
    reviews = {};
    $("#reviewContainer").empty();
    $("#username").val("");
});

const wayTop = document.getElementById('wayTop');

wayTop.addEventListener('click', () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
});
