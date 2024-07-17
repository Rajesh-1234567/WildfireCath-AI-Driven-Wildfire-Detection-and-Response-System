window.onscroll = function() {stickNavbar()};

const navbar = document.getElementById("navbar");
const sticky = navbar.offsetTop;

function stickNavbar() {
  if (window.pageYOffset > sticky) {
    navbar.classList.add("sticky");
  } else {
    navbar.classList.remove("sticky");
  }
}

// Slider functionality
const slides = document.querySelector('.slides');
const slide = document.querySelectorAll('.slide');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

let index = 0;

function showSlide(n) {
  index += n;
  if (index >= slide.length) {
    index = 0;
  }
  if (index < 0) {
    index = slide.length - 1;
  }
  slides.style.transform = 'translateX(' + (-index * 100) + '%)';
}

prevBtn.addEventListener('click', () => showSlide(-1));
nextBtn.addEventListener('click', () => showSlide(1));