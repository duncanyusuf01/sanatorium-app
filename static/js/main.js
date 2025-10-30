document.addEventListener('DOMContentLoaded', () => {

    /**
     * Pre-loader functionality
     */
    const preloader = document.querySelector('.preloader');
    
    window.addEventListener('load', () => {
        // Wait for the CSS logo animation to finish (2.5s)
        setTimeout(() => {
            if (preloader) {
                // Add class to trigger the 0.5s fade-out transition
                preloader.classList.add('fade-out');
            }
        }, 2500); // Matches CSS animation-duration

        // After the fade-out transition (0.5s), set display to none
        setTimeout(() => {
            if (preloader) {
                preloader.style.display = 'none';
            }
        }, 3000); // 2.5s animation + 0.5s fade-out
    });


    /**
     * Product Page Filtering
     */
    const filterContainer = document.querySelector('.filter-nav');
    const productItems = document.querySelectorAll('#product-gallery .product-item');

    if (filterContainer && productItems.length > 0) {
        
        filterContainer.addEventListener('click', (e) => {
            // Only act on button clicks
            if (!e.target.classList.contains('filter-btn')) {
                return;
            }

            // Remove 'active' class from all buttons
            filterContainer.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Add 'active' class to the clicked button
            const filterButton = e.target;
            filterButton.classList.add('active');
            
            const filterValue = filterButton.dataset.filter;

            // Loop through all product items and show/hide
            productItems.forEach(item => {
                const itemCategory = item.dataset.category;

                if (filterValue === 'all' || filterValue === itemCategory) {
                    item.classList.remove('hide');
                } else {
                    item.classList.add('hide');
                }
            });
        });
    }

});
