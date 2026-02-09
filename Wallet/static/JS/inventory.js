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

  // ========== ACTION MENU FUNCTIONALITY ==========

  // Function to position menu
  function positionMenu(button, menu) {
    const buttonRect = button.getBoundingClientRect();
    const menuWidth = 160;

    // Position below button, aligned to right
    menu.style.top = buttonRect.bottom + 4 + 'px';
    menu.style.left = buttonRect.right - menuWidth + 'px';
  }

  // Toggle dropdown menu for Available Items
  document.addEventListener('click', function (e) {
    // Check if clicked element is an action button
    if (e.target.classList.contains('action-btn')) {
      e.stopPropagation();

      // Close all other menus and remove active class from buttons
      document.querySelectorAll('.action-menu').forEach(function (menu) {
        if (menu !== e.target.nextElementSibling) {
          menu.classList.remove('show');
          if (menu.previousElementSibling) {
            menu.previousElementSibling.classList.remove('active');
          }
        }
      });

      // Toggle current menu and active class
      const menu = e.target.nextElementSibling;
      if (menu) {
        const isOpening = !menu.classList.contains('show');
        menu.classList.toggle('show');
        e.target.classList.toggle('active');

        // Position menu when opening
        if (isOpening) {
          positionMenu(e.target, menu);
        }
      }
    }
    // Check if clicked element is a menu item
    else if (e.target.classList.contains('menu-item')) {
      const action = e.target.getAttribute('data-action');
      const row = e.target.closest('tr');
      const itemId = row.querySelector('.item-id').textContent;
      const itemName = row.querySelector('.item-name').textContent;

      // Close the menu and remove active class
      const menu = e.target.closest('.action-menu');
      menu.classList.remove('show');
      if (menu.previousElementSibling) {
        menu.previousElementSibling.classList.remove('active');
      }

      // Handle the action
      handleItemAction(action, itemId, itemName, row);
    }
    // Close all menus when clicking outside
    else {
      document.querySelectorAll('.action-menu').forEach(function (menu) {
        menu.classList.remove('show');
        if (menu.previousElementSibling) {
          menu.previousElementSibling.classList.remove('active');
        }
      });
    }
  });

  // Reposition menus on scroll
  document.addEventListener(
    'scroll',
    function () {
      document.querySelectorAll('.action-menu.show').forEach(function (menu) {
        if (menu.previousElementSibling) {
          positionMenu(menu.previousElementSibling, menu);
        }
      });
    },
    true,
  );

  // Handle menu item actions
  function handleItemAction(action, itemId, itemName, row) {
    switch (action) {
      case 'add':
        console.log('Add Item:', itemId, itemName);
        alert('Add Item: ' + itemName + ' (' + itemId + ')');
        break;

      case 'request':
        console.log('Request Note:', itemId, itemName);
        alert('Request Note for: ' + itemName + ' (' + itemId + ')');
        break;

      case 'comment':
        console.log('Leave Comment:', itemId, itemName);
        alert('Leave Comment on: ' + itemName + ' (' + itemId + ')');
        break;
    }
  }
});

// Get filter elements
const statusFilter = document.getElementById('statusFilter');
const categoryFilter = document.getElementById('categoryFilter');
const searchInput = document.getElementById('itemSearch');

// Status Filter
statusFilter.addEventListener('change', function () {
  filterTable();
});

// Category Filter
categoryFilter.addEventListener('change', function () {
  filterTable();
});

// Search Filter
searchInput.addEventListener('input', function () {
  filterTable();
});

// Main filter function
function filterTable() {
  const selectedStatus = statusFilter.value;
  const selectedCategory = categoryFilter.value;
  const searchTerm = searchInput.value.toLowerCase();

  const tableRows = document.querySelectorAll('#itemsTableBody .table-row');

  tableRows.forEach((row) => {
    // Get data from the row
    const statusBadge = row.querySelector('.status-badge');
    const rowStatus = statusBadge.textContent.trim();

    const categoryCell = row.querySelector('td:nth-child(4)'); // "Other Names" column shows category
    const rowCategory = categoryCell.textContent.trim();

    const itemName = row.querySelector('.item-name').textContent.toLowerCase();
    const itemId = row.querySelector('.item-id').textContent.toLowerCase();

    // Check all filters
    const statusMatch =
      selectedStatus === 'all' || rowStatus === selectedStatus;
    const categoryMatch =
      selectedCategory === 'all' || rowCategory === selectedCategory;
    const searchMatch =
      searchTerm === '' ||
      itemName.includes(searchTerm) ||
      itemId.includes(searchTerm);

    // Show row only if ALL filters match
    if (statusMatch && categoryMatch && searchMatch) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
}
