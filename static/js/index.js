document.getElementById('loading').style.display = 'none';
const contentElement = document.getElementById('content');
contentElement.style.display = 'flex';
contentElement.style.flexDirection = 'column';

var firstHero = document.querySelector('.hero');
var secondHero = document.querySelector('#secondHero');
if (window.innerHeight < window.innerWidth) {
    firstHero.style.display = 'flex';
    secondHero.style.display = 'none';
} else {
    firstHero.style.display = 'none';
    secondHero.style.display = 'flex';
}

var description = document.querySelector('.description');
description.addEventListener('mouseover', function () {
    this.classList.add('glow-text');
});
description.addEventListener('mouseout', function () {
    this.classList.remove('glow-text');
});
