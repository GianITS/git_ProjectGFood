const menu = document.querySelector('.menu');
const menuContainer = document.querySelector('.containerMenu');
const menuContent = document.querySelector('.contentMenu');
const btnCloseMenu = document.getElementById('btnCloseMenu');

menu.onclick = function() {
    menuContainer.classList.add("showMenu");
    menuContent.classList.add("slideIn");
    menuContent.classList.remove("slideOut");
}

var delayInMilliseconds = 800;

btnCloseMenu.onclick = function() {
    menuContent.classList.remove("slideIn");
    menuContent.classList.add("slideOut");
    setTimeout(function() {
        menuContainer.classList.remove("showMenu");
    }, delayInMilliseconds);
}

