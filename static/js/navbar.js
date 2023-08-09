const hamburger = document.querySelector(".hamburger");
const navLinks = document.querySelector(".nav-links");
const links = document.querySelectorAll(".nav-links li");

hamburger.addEventListener('click', () => {
    //Animate Links
    navLinks.classList.toggle("open");
    links.forEach(link => {
        link.classList.toggle("fade");
    });

    //Hamburger Animation
    hamburger.classList.toggle("toggle");
});

document.addEventListener('DOMContentLoaded', function () {
    const navLinks = document.querySelectorAll('.nav-links li a');
    const lastActiveLink = localStorage.getItem('activeLink');

    if (lastActiveLink) {
        navLinks.forEach(link => link.classList.remove('active'));
        document.querySelector(`.nav-links li a[href="${lastActiveLink}"]`).classList.add('active');
    }

    navLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            localStorage.setItem('activeLink', event.target.getAttribute('href'));
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.querySelector('nav');
    const scrollThreshold = 100;

    window.addEventListener('scroll', function () {
        if (window.scrollY > scrollThreshold) {
            navbar.classList.add('nav-dark');
        } else {
            navbar.classList.remove('nav-dark');
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const loginBtn = document.querySelector('.login-btn');
    let originalListItem;
    let originalStyles;

    function replaceLoginBtn() {
        if (window.innerWidth < 800) {
            if (loginBtn) {
                const loginLink = loginBtn.getAttribute('href');
                const loginText = loginBtn.textContent;
                originalListItem = loginBtn.parentNode;
                originalStyles = getComputedStyle(originalListItem);

                const newListItem = document.createElement('li');
                newListItem.classList.add('fade');

                const newAnchor = document.createElement('a');
                newAnchor.setAttribute('href', loginLink);
                newAnchor.textContent = loginText;

                newListItem.appendChild(newAnchor);
                loginBtn.parentNode.replaceChild(newListItem, loginBtn);
            }
        } else {
            if (originalListItem) {
                const newAnchor = document.createElement('a');
                newAnchor.setAttribute('href', originalListItem.querySelector('a').getAttribute('href'));
                newAnchor.textContent = originalListItem.textContent;
                originalListItem.parentNode.replaceChild(newAnchor, originalListItem);
                originalListItem = null;
            }
        }
    }

    function handleResponsiveChanges() {
        replaceLoginBtn();
      }
    
      handleResponsiveChanges();
      window.addEventListener('resize', handleResponsiveChanges);
});
