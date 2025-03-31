// Select elements
const sliderList = document.querySelector('.slider .list');
const dots = document.querySelectorAll('.slider .dots li');
const prevButton = document.querySelector('#prev');
const nextButton = document.querySelector('#next');
const slides = document.querySelectorAll('.slider .list .item');
const carousel = document.querySelector('.carousel');
const items = document.querySelectorAll('.carousel .item');
const afPrevButton = document.querySelector('.af-prev');
const afNextButton = document.querySelector('.af-next');

// Initialize variables
let currentIndex = 0;
const totalSlides = slides.length;
let autoScroll;
let isTransitioning = false;

// Error handling for missing elements
if (!sliderList || !dots.length || !prevButton || !nextButton || !slides.length) {
    console.error('Required slider elements not found');
}

if (!carousel || !items.length || !afPrevButton || !afNextButton) {
    console.error('Required carousel elements not found');
}

// Function to update the slider
function updateSlider() {
    if (!sliderList || !slides.length) return;
    
    try {
        const offset = -currentIndex * 100;
        sliderList.style.transition = 'left 0.3s ease';
        sliderList.style.left = `${offset}%`;

        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentIndex);
        });

        slides.forEach((slide, index) => {
            slide.classList.toggle('middle', index === currentIndex);
        });
    } catch (error) {
        console.error('Error updating slider:', error);
    }
}

// Function to change slides
function changeSlide(direction) {
    if (isTransitioning) return;
    
    try {
        isTransitioning = true;
        currentIndex = (currentIndex + direction + totalSlides) % totalSlides;
        updateSlider();
        
        // Reset transition flag after animation
        setTimeout(() => {
            isTransitioning = false;
        }, 300);
    } catch (error) {
        console.error('Error changing slide:', error);
        isTransitioning = false;
    }
}

// Event listeners for navigation
if (nextButton) {
    nextButton.addEventListener('click', () => changeSlide(1));
}

if (prevButton) {
    prevButton.addEventListener('click', () => changeSlide(-1));
}

dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
        if (isTransitioning) return;
        currentIndex = index;
        updateSlider();
    });
});

// Auto-slide
setInterval(() => changeSlide(1), 3000);

// Carousel scrolling
function scrollCarousel(direction) {
    if (!carousel || !items.length) return;
    
    try {
        const itemWidth = items[0].offsetWidth + 20;
        carousel.scrollBy({ left: direction * itemWidth, behavior: 'smooth' });
        resetAutoScroll();
    } catch (error) {
        console.error('Error scrolling carousel:', error);
    }
}

function autoMove() {
    if (!carousel || !items.length) return;
    
    try {
        const itemWidth = items[0].offsetWidth + 20;
        if (carousel.scrollLeft + carousel.clientWidth >= carousel.scrollWidth) {
            carousel.scrollTo({ left: 0, behavior: 'smooth' });
        } else {
            carousel.scrollBy({ left: itemWidth, behavior: 'smooth' });
        }
    } catch (error) {
        console.error('Error in auto move:', error);
    }
}

function resetAutoScroll() {
    clearInterval(autoScroll);
    autoScroll = setInterval(autoMove, 3000);
}

// Event listeners for manual scrolling
if (afPrevButton) {
    afPrevButton.addEventListener('click', () => scrollCarousel(-1));
}

if (afNextButton) {
    afNextButton.addEventListener('click', () => scrollCarousel(1));
}

// Initialize auto-scroll
if (carousel && items.length) {
    autoScroll = setInterval(autoMove, 3000);
}

// Cleanup function
function cleanup() {
    clearInterval(autoScroll);
    // Remove event listeners
    if (nextButton) {
        nextButton.removeEventListener('click', () => changeSlide(1));
    }
    if (prevButton) {
        prevButton.removeEventListener('click', () => changeSlide(-1));
    }
    if (afPrevButton) {
        afPrevButton.removeEventListener('click', () => scrollCarousel(-1));
    }
    if (afNextButton) {
        afNextButton.removeEventListener('click', () => scrollCarousel(1));
    }
}

// Cleanup on page unload
window.addEventListener('unload', cleanup);
