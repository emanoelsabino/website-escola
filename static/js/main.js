/**
* Template Name: Mentor
* Template URL: https://bootstrapmade.com/mentor-free-education-bootstrap-theme/
* Updated: Mar 19 2024 with Bootstrap v5.3.3
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  mobileNavToggleBtn.addEventListener('click', mobileNavToogle);

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .has-dropdown i').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      if (document.querySelector('.mobile-nav-active')) {
        e.preventDefault();
        this.parentNode.classList.toggle('active');
        this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
        e.stopImmediatePropagation();
      }
    });
  });

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Initiate Pure Counter
   */
  new PureCounter();

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll('.swiper').forEach(function(swiper) {
      let config = JSON.parse(swiper.querySelector('.swiper-config').innerHTML.trim());
      new Swiper(swiper, config);
    });
  }
  window.addEventListener('load', initSwiper);

})();


/**
 * Meus scripts
 */
function sortTable(colIndex) {
  var table = document.getElementById("table");
  var rows = table.rows;
  var switching = true;

  while (switching) {
      switching = false;
      for (var i = 1; i < rows.length - 1; i++) {
          var row1 = rows[i].getElementsByTagName("td")[colIndex];
          var row2 = rows[i + 1].getElementsByTagName("td")[colIndex];
          
          // Convertendo os valores para números antes de compará-los
          var value1 = isNaN(parseFloat(row1.innerHTML)) ? row1.innerHTML.toLowerCase() : parseFloat(row1.innerHTML);
          var value2 = isNaN(parseFloat(row2.innerHTML)) ? row2.innerHTML.toLowerCase() : parseFloat(row2.innerHTML);
          
          if (value1 > value2) {
              rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
              switching = true;
              break;
          }
      }
  }
}

/**
 * Paginação da tabela
 */
document.addEventListener('DOMContentLoaded', function () {
  var table = document.getElementById('table');
  var tableRows = table.getElementsByTagName('tr');
  var totalPages = Math.ceil((tableRows.length - 1) / 10); // Assuming each page shows 5 rows
  var pagination = document.querySelector('.pagination');

  function showPage(page) {
    for (var i = 1; i < tableRows.length; i++) {
      tableRows[i].style.display = 'none';
    }
    for (var i = (page - 1) * 10 + 1; i < page * 10 + 1; i++) {
      if (tableRows[i]) {
        tableRows[i].style.display = 'table-row';
      }
    }
  }

  function setupPagination() {
    pagination.innerHTML = '';

    for (var i = 1; i <= totalPages; i++) {
      var li = document.createElement('li');
      li.textContent = i;

      li.addEventListener('click', function () {
        var pageNumber = parseInt(this.textContent);
        showPage(pageNumber);
        var active = document.querySelector('.pagination li.active');
        if (active) active.classList.remove('active');
        this.classList.add('active');
      });

      pagination.appendChild(li);
    }

    showPage(1);
    pagination.firstElementChild.classList.add('active');
  }

  setupPagination();
});


/**
 * Mensagem temporaria de 3 segundos
 */
setTimeout(function() {
  document.getElementById('flash-message').style.display = 'none';
}, 5000);
