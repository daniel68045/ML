// Event listener to listen for clicks on browser and button clicks with web app
document.addEventListener("DOMContentLoaded", () => {
  const authorizeBtn = document.getElementById("authorize-btn");
  const loadingScreen = document.getElementById("loading-screen");

  if (authorizeBtn && loadingScreen) {
    loadingScreen.classList.add("hidden");

    authorizeBtn.addEventListener("click", () => {
      loadingScreen.classList.remove("hidden");

      history.pushState({ page: "auth" }, "Spotify Auth", "/login");
      window.location.href = "/login";
    });
  } else {
    console.log("Authorize button or loading screen not found");
  }

  window.addEventListener("popstate", (event) => {
    if (loadingScreen) {
      loadingScreen.classList.add("hidden");
    }

    if (event.state && event.state.page === "auth") {
    }
  });
});
