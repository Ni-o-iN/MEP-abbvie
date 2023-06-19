//BEREICHE ANZEIGEN BEI MAUSBERÜHRUNG
var areas = document.querySelectorAll('.area');
// = document.getElementByClass('tooltip');

areas.forEach(function (area) {
    area.addEventListener('mousemove', function (event) {
        var areaName = area.getAttribute('data-name');
        tooltip.innerText = areaName;
        tooltip.style.top = event.clientY + 'px';
        tooltip.style.left = event.clientX + 'px';
        tooltip.style.display = 'block';
    });

    area.addEventListener('mouseleave', function () {
        tooltip.style.display = 'none';
    });
});

//Info
// Wenn der Info-Button geklickt wird, öffnet sich das Hilfe-Fenster
// document.getElementById("infoButton").addEventListener("click", function () {
//     document.getElementById("infoModal").style.display = "block";
// });

// // Wenn das Schließen-Symbol oder der Hintergrund des Info-Fensters geklickt wird, wird es geschlossen
// document.getElementsByClassName("close")[0].addEventListener("click", function () {
//     document.getElementById("infoModal").style.display = "none";
// });

window.onclick = function (event) {
    if (event.target == document.getElementById("infoModal")) {
        document.getElementById("infoModal").style.display = "none";
    }
};


/*Hamburger Menü*/
function toggleMenu() {
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const menuIcons = document.querySelector('.menu-icons');
    hamburgerMenu.classList.toggle('open');
    menuIcons.classList.toggle('open');
}

window.addEventListener('resize', function () {
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const menuIcons = document.querySelector('.menu-icons');
    if (window.innerWidth > 1300) {
        hamburgerMenu.classList.remove('open');
        menuIcons.classList.remove('open');
    }
});