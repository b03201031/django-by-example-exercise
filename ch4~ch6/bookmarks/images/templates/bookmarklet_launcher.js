(function () {
    if (window.myBookmarklet !== undefined) {
        myBookmarklet()
    }
    else {
        document.body.appendChild(document.createElement('script')).src = 'https://a7792419.ngrok.io/static/images/js/bookmarklet.js?r=' + Math.floor(Math.random() * 99999999999999999999);
    }
})();