document.addEventListener('DOMContentLoaded', function () {
var modeSwitch = document.querySelector('.mode-switch');

modeSwitch.addEventListener('click', function () {document.documentElement.classList.toggle('dark');
modeSwitch.classList.toggle('active');
});

var listView = document.querySelector('.list-view');
var gridView = document.querySelector('.grid-view');
var projectsList = document.querySelector('.project-boxes');
var sidebarLinks = document.querySelectorAll('.app-sidebar-link');
sidebarLinks.forEach(function (link) {
    link.addEventListener('click', function (event) {
        event.preventDefault(); // Забороняємо стандартну дію посилання
        sidebarLinks.forEach(function (l) {
            l.classList.remove('active');
        });
        this.classList.add('active');

        var id = this.getAttribute('id'); // Отримуємо id кнопки
        var url = this.getAttribute('href'); // Отримуємо URL посилання
        fetch(url + "/menu/" + id) // Відправляємо GET запит на вказаний URL з id
            .then(response => response.text()) // Отримуємо відповідь у вигляді тексту
            .then(data => {
                document.querySelector('.projects-section').innerHTML = data; // Змінюємо HTML контент вмісту projects-section
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

document.querySelector('.messages-btn').addEventListener('click', function () {
document.querySelector('.messages-section').classList.add('show');
});

document.querySelector('.messages-close').addEventListener('click', function() {
document.querySelector('.messages-section').classList.remove('show');
});
});
