import { invoke } from "@tauri-apps/api/core";

document.addEventListener("DOMContentLoaded", () => {

  const loginScreen = document.getElementById("login-screen");
  const mainApp = document.getElementById("main-app");

  const loginBtn = document.getElementById("login-btn");
  const loginGroup = loginBtn.closest(".group"); // full login section
  const linkGroup = document.querySelector(".group.center"); // warframe link section
  const bottomRow = document.getElementById("bottom-items");

  // ✅ CHECK IF FIRST RUN OR NOT
  (async () => {
    try {
      const isSetup = await invoke("is_setup_complete");

      if (!isSetup) {
        // FIRST RUN → show login
        mainApp.style.display = "none";

        loginScreen.appendChild(loginGroup);
        loginScreen.appendChild(linkGroup);

      } else {
        // RETURNING USER → skip login
        loginScreen.style.display = "none";
        mainApp.style.display = "block";

        bottomRow.appendChild(loginGroup);
        bottomRow.appendChild(linkGroup);
      }

    } catch (err) {
      console.error("Failed to check setup state:", err);
    }
  })();


  
  // STEP 1: Move existing elements to login screen
  loginScreen.appendChild(loginGroup);
  loginScreen.appendChild(linkGroup);

  // Hide main UI initially
  mainApp.style.display = "none";

  // STEP 2: Hook into EXISTING login button
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

  





  const saveBtn = document.getElementById("greet-save-btn");

  saveBtn.addEventListener("click", async () => {
    const input = document.getElementById("greet-input");
    const value = input.value;

    if (value.trim() === "") return;

    try {
      // 1. Save link FIRST
      await invoke("save_warframe_link", { value });
      console.log("Warframe link saved");

      // ⚠️ IMPORTANT: remove this if you don’t have it in Rust
      // await invoke("close_browser");

      // 2. Move elements back
      bottomRow.appendChild(loginGroup);
      bottomRow.appendChild(linkGroup);

      // 3. Switch UI
      loginScreen.style.display = "none";
      mainApp.style.display = "block";

    } catch (err) {
      console.error("Error during onboarding transition:", err);
    }
  });

  // MIN PLAT SAVE
  document.getElementById("min-plat-save").addEventListener("click", async () => {
    const value = parseInt(document.getElementById("min-plat-input").value);
    if (!isNaN(value)) {
      await invoke("save_min_plat_price", { value });
      console.log("Min plat price saved");
    }
  });

  // DELETE ALL MODS
  document.getElementById("delete-all-mods-btn").addEventListener("click", async () => {
    // For DeleteAllMods, we just call handle_button_click with action "delete_all_mods"
    const item = ""; // No specific item, since it's global
    const action = "delete_all_mods";

    console.log("Sending delete all mods request to backend...");

    try {
      await invoke("handle_button_click", { item, action });
      console.log("DeleteAllMods invoked successfully.");
    } catch (err) {
      console.error("Error invoking DeleteAllMods:", err);
    }
  });

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