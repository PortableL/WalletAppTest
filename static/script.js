const tabButtons = document.querySelectorAll(".tab");
const tabContents = {
  0: document.getElementById("wallet-content"),
  1: document.getElementById("save-content"),
  2: document.getElementById("borrow-content"),
  3: document.getElementById("grow-content"),
};

const iconsDefault = document.getElementById("icons-default");
const iconsBorrow = document.getElementById("icons-borrow");

// Function to activate a tab by index
function activateTab(index) {
  // Remove active styles from all tabs
  tabButtons.forEach((t) => {
    t.classList.remove("bg-[#0052ff]", "text-white", "rounded-t-xl");
    t.classList.add("bg-white", "text-[#0a2e79]");
  });

  // Hide all content sections
  Object.values(tabContents).forEach((content) => {
    if (content) content.classList.add("hidden");
  });

  // Add active styles to clicked tab
  const tab = tabButtons[index];
  tab.classList.add("bg-[#0052ff]", "text-white", "rounded-t-xl");
  tab.classList.remove("bg-white", "text-[#0a2e79]");

  // Show the corresponding content
  const activeContent = tabContents[index];
  if (activeContent) activeContent.classList.remove("hidden");

  // Toggle icons depending on the tab
  if (index === 2) { // Borrow tab
    iconsDefault?.classList.add("hidden");
    iconsBorrow?.classList.remove("hidden");
  } else {
    iconsDefault?.classList.remove("hidden");
    iconsBorrow?.classList.add("hidden");
  }

  // Save active tab index in localStorage
  localStorage.setItem("activeTabIndex", index);
}

// Add click listeners for all tabs
tabButtons.forEach((tab, index) => {
  tab.addEventListener("click", () => {
    activateTab(index);
  });
});

// On page load, restore last active tab (default to 0 = Wallet)
window.addEventListener("load", () => {
  const savedIndex = localStorage.getItem("activeTabIndex");
  const index = savedIndex ? parseInt(savedIndex) : 0;
  activateTab(index);
});

// Toggle savings visibility
const toggleButton = document.getElementById("toggle-savings");
const savingsAmount = document.getElementById("savings-amount");
const eyeOpenIcon = document.getElementById("eye-open-icon");
const eyeClosedIcon = document.getElementById("eye-closed-icon");

if (toggleButton && savingsAmount && eyeOpenIcon && eyeClosedIcon) {
  toggleButton.addEventListener("click", () => {
    const isHidden = savingsAmount.textContent.includes("*");

    if (isHidden) {
      savingsAmount.textContent = "10.00"; // Replace with dynamic value if needed
      eyeOpenIcon.classList.add("hidden");
      eyeClosedIcon.classList.remove("hidden");
    } else {
      savingsAmount.textContent = "*********";
      eyeOpenIcon.classList.remove("hidden");
      eyeClosedIcon.classList.add("hidden");
    }
  });
}






















