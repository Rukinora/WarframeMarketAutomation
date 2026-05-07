// console.log("JS loaded");
// import { invoke } from "@tauri-apps/api/core";

// document
//   .getElementById("time-save-btn")
//   .addEventListener("click", async () => {
//     console.log("BUTTON CLICKED");

//     const timeValue = parseFloat(
//       document.getElementById("time-input").value
//     );

//     console.log("Time value:", timeValue);

//     try {
//       await invoke("save_time", { value: timeValue });
//       console.log("Invoke sent");
//     } catch (error) {
//       console.error("Error saving:", error);
//     }
//   });