document.addEventListener('scroll', function() {
    const parallaxContainers = document.getElementsByClassName('parallax-container');

    //Calculate scroll ratio
    const scrolled = window.scrollY / 2;

    //Testing
    //console.log(parallaxContainers.length);

    for (var i = 0; i < parallaxContainers.length; i++) {
        // Apply the parallax effect
        parallaxContainers[i].style.backgroundPosition = 'center ' + -scrolled + 'px';
    }
});
