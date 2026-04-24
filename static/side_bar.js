function openNav() {
  document.getElementById("side_menu").style.width = "200px";
  const overlay = document.getElementById("sidebar_overlay");
  if (overlay) overlay.classList.add("active");
}

function closeNav() {
  document.getElementById("side_menu").style.width = "0";
  const overlay = document.getElementById("sidebar_overlay");
  if (overlay) overlay.classList.remove("active");
}

// Close sidebar on Escape key
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") closeNav();
});