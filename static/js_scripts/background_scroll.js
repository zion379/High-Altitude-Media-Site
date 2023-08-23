document.addEventListener('scroll', function() {
    const parallaxContainer = document.querySelector('.parallax-container');

    //Calculate scroll ratio
    const scrolled = window.scrollY / 5;

    // Apply the parallax effect
    parallaxContainer.style.backgroundPosition = 'center ' + -scrolled + 'px';
});
