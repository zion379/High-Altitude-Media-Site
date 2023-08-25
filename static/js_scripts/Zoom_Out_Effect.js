document.addEventListener('scroll', function() {
    const zoomContainer = document.querySelector('.zoom-out-effect');
    // Get Back Ground Image Current Size
    let currentSize = parseInt(window.getComputedStyle(zoomContainer, null).getPropertyValue('background-size'));
    
    let scrolled = window.scrollY
    console.log(scrolled)

    if(parseInt(window.getComputedStyle(zoomContainer).getPropertyValue('background-size')) >= 100) {
        currentSize -= 1;
        //console.log('Zooming in');
    }
    console.log( parseInt(window.getComputedStyle(zoomContainer).getPropertyValue('background-size')));

    zoomContainer.style.backgroundSize = currentSize + '%';
});