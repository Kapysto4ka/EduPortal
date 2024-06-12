
document.addEventListener('DOMContentLoaded', function () {
    var modeSwitch = document.querySelector('.mode-switch');

    modeSwitch.addEventListener('click', function () {document.documentElement.classList.toggle('dark');
    modeSwitch.classList.toggle('active');

    });

    document.querySelectorAll('.project-box').forEach(item => {
        item.addEventListener('click', event => {
        window.location.href = item.getAttribute('data-href');
        });
    });
    var listView = document.querySelector('.list-view');
    var gridView = document.querySelector('.grid-view');
    var projectsList = document.querySelector('.project-boxes');
    var sidebarLinks = document.querySelectorAll('.app-sidebar-link');
    sidebarLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            sidebarLinks.forEach(function (l) {
                l.classList.remove('active');
            });
            this.classList.add('active');

            var id = this.getAttribute('id'); 
            if (id === 'home') {
                location.reload();
                return;
            }
            var url = this.getAttribute('href'); 
            fetch(url + "/menu/" + id) 
                .then(response => response.text()) 
                .then(data => {
                    document.querySelector('.projects-section').innerHTML = data; 
                })
                .catch(error => console.error('Error:', error));
        });
    });

    listView.addEventListener('click', function () {
    gridView.classList.remove('active');
    listView.classList.add('active');
    projectsList.classList.remove('jsGridView');
    projectsList.classList.add('jsListView');
    });

    gridView.addEventListener('click', function () {
    gridView.classList.add('active');
    listView.classList.remove('active');
    projectsList.classList.remove('jsListView');
    projectsList.classList.add('jsGridView');
    });


    const sidebar = document.querySelector('.app-sidebar');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const projectsSection = document.querySelector('.projects-section');
    
    let isSidebarVisible = true; 
    
    sidebarToggle.addEventListener('click', function () {
        if (isSidebarVisible) {
            sidebar.remove();
        } else {
            projectsSection.insertAdjacentElement('beforebegin', sidebar); 
        }
    
        isSidebarVisible = !isSidebarVisible; 
    });
    
});
