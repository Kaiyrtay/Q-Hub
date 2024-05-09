document.addEventListener("DOMContentLoaded", function () {
  const darkModeSwitch = document.getElementById("darkModeSwitch");

  function setDarkMode(isDarkMode) {
    if (isDarkMode) {
      document.body.classList.add("dark-mode");
      localStorage.setItem("dark-mode", "true");
    } else {
      document.body.classList.remove("dark-mode");
      localStorage.setItem("dark-mode", "false");
    }
  }

  darkModeSwitch.addEventListener("change", function () {
    setDarkMode(this.checked);
  });

  // Initialize dark mode based on local storage
  const isDarkMode = localStorage.getItem("dark-mode") === "true";
  darkModeSwitch.checked = isDarkMode;
  setDarkMode(isDarkMode);
});
