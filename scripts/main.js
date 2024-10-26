const icon = document.querySelector(".chaticon");
const chat = document.querySelector(".chat");

icon.addEventListener("click", () => {
  chat.classList.toggle("visible");
  icon.classList.toggle("expanded");
});
