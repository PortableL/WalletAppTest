document.addEventListener('DOMContentLoaded', function () {
  // Get all nav buttons
  const navButtons = document.querySelectorAll('.nav-link');

  // Function to remove active class from all buttons
  function removeActiveClass() {
    navButtons.forEach((btn) => btn.classList.remove('active'));
  }

  // Function to show content based on which button was clicked
  function showContent(contentId) {
    // Hide all content sections
    const allSections = document.querySelectorAll('.content-section');
    allSections.forEach((section) => (section.style.display = 'none'));

    // Show the selected content
    const selectedSection = document.getElementById(contentId);
    if (selectedSection) {
      selectedSection.style.display = 'block';
    }
  }

  // Home button
  document.getElementById('homeBtn').addEventListener('click', function () {
    removeActiveClass();
    this.classList.add('active');
    showContent('homeContent');
  });

  // Category button
  document.getElementById('categoryBtn').addEventListener('click', function () {
    removeActiveClass();
    this.classList.add('active');
    showContent('categoryContent');
  });

  // Available Items button
  document
    .getElementById('availableItemsBtn')
    .addEventListener('click', function () {
      removeActiveClass();
      this.classList.add('active');
      showContent('availableItemsContent');
    });

  // Add Items button
  document.getElementById('addItemsBtn').addEventListener('click', function () {
    removeActiveClass();
    this.classList.add('active');
    showContent('addItemsContent');
  });

  // Cancelled Items button
  document
    .getElementById('cancelledItemsBtn')
    .addEventListener('click', function () {
      removeActiveClass();
      this.classList.add('active');
      showContent('cancelledItemsContent');
    });

  // Transaction History button
  document
    .getElementById('transactionHistoryBtn')
    .addEventListener('click', function () {
      removeActiveClass();
      this.classList.add('active');
      showContent('transactionHistoryContent');
    });

  // Settings button
  document.getElementById('settingsBtn').addEventListener('click', function () {
    removeActiveClass();
    this.classList.add('active');
    showContent('settingsContent');
  });

  // Logout button
  document.getElementById('logoutBtn').addEventListener('click', function () {
    // Redirect to logout route
    window.location.href = '/logout';
  });
});
