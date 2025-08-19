 function showLoader() {
        document.getElementById('loader-bar').style.display = 'block';
    }


    window.addEventListener('pageshow', function () {
        document.getElementById('loader-bar').style.display = 'none';
    });