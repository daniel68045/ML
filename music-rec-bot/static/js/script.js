// Event listener to listen for clicks on browser and button clicks with web app
document.addEventListener("DOMContentLoaded", () => {
  const authorizeBtn = document.getElementById("authorize-btn");
  const loadingScreen = document.getElementById("loading-screen");

  // Handle initial page & initial click
  if (authorizeBtn && loadingScreen) {
    loadingScreen.classList.add("hidden"); // Start with the screen hidden

    authorizeBtn.addEventListener("click", () => {
      loadingScreen.classList.remove("hidden"); // Show the loading screen

      // Push a state to history before navigating
      history.pushState({ page: "auth" }, "Spotify Auth", "/login");
      window.location.href = "/login";
    });
  } else {
    console.log("Authorize button or loading screen not found"); // If screen is not found - error incase CSS changes
  }

  // Handle browser back/forward navigation
  window.addEventListener("popstate", (event) => {
    if (loadingScreen) {
      loadingScreen.classList.add("hidden"); // Hide the loading screen
    }

    // Handle other states if necessary
    if (event.state && event.state.page === "auth") {
    }
  });
});
