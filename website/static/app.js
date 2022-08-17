const menu = document.querySelector('.menu');
const menuContainer = document.querySelector('.containerMenu');
const menuContent = document.querySelector('.contentMenu');
const btnCloseMenu = document.getElementById('btnCloseMenu');
const user = document.querySelector('.imgUser');
const userMenu = document.querySelector('.userMenu');

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

user.onclick = function() {
    userMenu.classList.toggle("showUserMenu");
}

const idUserMenu = document.getElementById('userMenu');

document.onclick = function(e){
    if (e.target !== user && e.target.id !== 'userMenu'){
        userMenu.classList.remove("showUserMenu");
    }
}

const toTop = document.querySelector(".goUp")

window.addEventListener("scroll", () =>{
    toTop.classList.toggle("active", window.scrollY > 200);
})