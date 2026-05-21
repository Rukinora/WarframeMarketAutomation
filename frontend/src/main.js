import { invoke } from "@tauri-apps/api/core";

// Initialize behavior after the DOM is ready.
document.addEventListener("DOMContentLoaded", () => {

  // Root UI containers
  const loginScreen = document.getElementById("login-screen");
  const mainApp = document.getElementById("main-app");

  // Elements used to control onboarding and actions
  const loginBtn = document.getElementById("login-btn");
  const loginGroup = loginBtn.closest(".group"); // grouping that contains login UI
  const linkGroup = document.querySelector(".group.center"); // warframe link input group
  const bottomRow = document.getElementById("bottom-items"); // area for main app controls

  // Immediately check with the backend whether initial setup is complete.
  // The backend RPC `is_setup_complete` returns a boolean. Based on that we
  // either show the onboarding (login screen) or the main app UI.
  (async () => {
    try {
      const isSetup = await invoke("is_setup_complete");

      if (!isSetup) {
        // First run: hide main app and ensure onboarding groups are visible
        mainApp.style.display = "none";

        loginScreen.appendChild(loginGroup);
        loginScreen.appendChild(linkGroup);

      } else {
        // Returning user: show main app and move groups into the bottom row
        loginScreen.style.display = "none";
        mainApp.style.display = "block";

        bottomRow.appendChild(loginGroup);
        bottomRow.appendChild(linkGroup);
      }

    } catch (err) {
      console.error("Failed to check setup state:", err);
    }
  })();


  // Ensure onboarding groups are placed in the login screen by default and
  // keep the main UI hidden until we explicitly show it.
  loginScreen.appendChild(loginGroup);
  loginScreen.appendChild(linkGroup);

  mainApp.style.display = "none";

  // Clicking the login button triggers a backend action that opens the
  // browser / starts the OAuth flow. We call the generic `handle_button_click`
  // RPC with an action of "login" so the Rust backend can handle it.
  loginBtn.addEventListener("click", async () => {
    try {
      await invoke("handle_button_click", {
        item: "",
        action: "login"
      });
    } catch (err) {
      console.error("Failed to open browser:", err);
    }
  });


  // Save button for the Warframe link (onboarding). Reads the input value,
  // sends it to the backend via `save_warframe_link`, then moves the UI into
  // the main app state.
  const saveBtn = document.getElementById("greet-save-btn");

  saveBtn.addEventListener("click", async () => {
    const input = document.getElementById("greet-input");
    const value = input.value;

    if (value.trim() === "") return;

    try {
      await invoke("save_warframe_link", { value });
      console.log("Warframe link saved");

      // Move the onboarding groups into the bottom row for the main UI
      bottomRow.appendChild(loginGroup);
      bottomRow.appendChild(linkGroup);

      // Switch visible panes: hide onboarding, show main app
      loginScreen.style.display = "none";
      mainApp.style.display = "block";

    } catch (err) {
      console.error("Error during onboarding transition:", err);
    }
  });

  // Save minimum plat price: reads numeric input and forwards to backend.
  document.getElementById("min-plat-save").addEventListener("click", async () => {
    const value = parseInt(document.getElementById("min-plat-input").value);
    if (!isNaN(value)) {
      await invoke("save_min_plat_price", { value });
      console.log("Min plat price saved");
    }
  });

  // Delete all mods button: sends a specific action to the backend handler.
  document.getElementById("delete-all-mods-btn").addEventListener("click", async () => {
    const item = "";
    const action = "delete_all_mods";

    console.log("Sending delete all mods request to backend...");

    try {
      await invoke("handle_button_click", { item, action });
      console.log("DeleteAllMods invoked successfully.");
    } catch (err) {
      console.error("Error invoking DeleteAllMods:", err);
    }
  });

  // Generic per-item action buttons: each `.box-btn` must have a data-action
  // and be contained in a `.box` which has a data-item. Clicking forwards
  // these to the backend via `handle_button_click`.
  document.querySelectorAll(".box-btn").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      const action = e.target.dataset.action;
      const item = e.target.closest(".box").dataset.item;

      console.log("Sending to backend:", item, action);

      await invoke("handle_button_click", {
        item: item,
        action: action
      });
    });
  });


});