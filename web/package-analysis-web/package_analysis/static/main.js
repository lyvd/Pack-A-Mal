document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;
    const themeDefault = document.getElementById('theme-default');
    const themeCyborg = document.getElementById('theme-cyborg');
    const themeNight = document.getElementById('theme-night');

    themeDefault.addEventListener('click', function(event) {
        event.preventDefault();
        body.className = ''; 
    });

    themeCyborg.addEventListener('click', function(event) {
        event.preventDefault();
        body.className = 'cyborg'; 
    });

    themeNight.addEventListener('click', function(event) {
        event.preventDefault();
        body.className = 'night'; 
    });
});

