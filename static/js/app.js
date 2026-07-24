const menuBtn = document.querySelector(".menu-btn");
const mobileMenu = document.querySelector(".mobile-menu");
const closeMenu = document.querySelector(".close-menu");

menuBtn.addEventListener("click", () => {

    mobileMenu.classList.add("active");

});

closeMenu.addEventListener("click", () => {

    mobileMenu.classList.remove("active");

});



document.querySelectorAll(".close-flash").forEach(btn=>{

btn.addEventListener("click",()=>{

btn.parentElement.remove();

});

});

setTimeout(()=>{

document.querySelectorAll(".flash-message").forEach(msg=>{

msg.remove();

});

},1000);
