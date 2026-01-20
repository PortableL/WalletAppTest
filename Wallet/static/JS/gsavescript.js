document.addEventListener('DOMContentLoaded', function () {
  const tabHub = document.getElementById('tab-hub');
  const tabSavings = document.getElementById('tab-savings');
  const hubContent = document.getElementById('hub-content');
  const mySavingsContent = document.getElementById('mysavings-content');
  const tabs = [tabHub, tabSavings];

  function activateTab(activeTab) {
    tabs.forEach((tab) => {
      if (tab === activeTab) {
        tab.classList.add(
          'border-blue-800',
          'text-blue-800',
          'font-bold',
          'transition-all',
          'duration-300'
        );
        tab.classList.remove('border-transparent', 'text-gray-500');
      } else {
        tab.classList.remove('border-blue-800', 'font-bold');
        tab.classList.add(
          'border-transparent',
          'text-gray-500',
          'transition-all',
          'duration-300'
        );
      }
    });
  }

  tabHub.addEventListener('click', function () {
    activateTab(tabHub);
    hubContent.classList.remove('hidden');
    mySavingsContent.classList.add('hidden');
  });

  tabSavings.addEventListener('click', function () {
    activateTab(tabSavings);
    mySavingsContent.classList.remove('hidden');
    hubContent.classList.add('hidden');
  });

  // Default to Hub tab
  activateTab(tabHub);
});
