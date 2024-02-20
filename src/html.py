index = '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous" />
<link href="https://fonts.googleapis.com/css?family=Cousine" rel="stylesheet">
<link href="https://fonts.googleapis.com/css?family=Noto+Sans+JP" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons%7CMaterial+Icons+Outlined" rel="stylesheet" />
<style>body { font-family: 'Cousine', 'Noto Sans JP', sans-serif; }</style>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.min.js" integrity="sha384-cuYeSxntonz0PPNlHhBs68uyIAVpIIOZZ5JqeqvYYIcEL727kskC66kF92t6Xl2V" crossorigin="anonymous"></script>
<title>リモコン</title>
<script>
const movePage = async(pageNum) => {
    url = `/api/1/page/${pageNum}`;
    const res = await fetch(url, {
        method: 'PUT',
    });
    return res.json();
};
const focusMenu = async() => {
    const res = await fetch('/api/1/page');
    res.json().then(e => document.getElementById(e.current_page).focus());
};
document.addEventListener('DOMContentLoaded', () => {
    focusMenu();
    const toast = document.getElementById('toast');
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast, {delay:1000});
    [...document.querySelectorAll('[name="movePageTo"]')].forEach(e => {
        e.addEventListener('click', (event) => {
            movePage(event.currentTarget.id).then(_ => toastBootstrap.show());
        });
    });
});
</script>
</head>
<body>
<div class="container-fluid pt-3"><div class="row"><div class="col-12 position-absolute bottom-0 mb-3 text-end">
    <a href="/api/1/log" target="_blank" class="btn btn-secondary mb-2">ログ</a>
    <div class="d-grid">
        <div class="btn-group-vertical" role="group" aria-label="リモコン">
            <button type="button" id="0" name="movePageTo" class="btn btn-outline-success btn-lg">
                <span class="material-icons align-middle fs-1 me-1 mb-1">home</span><span class="align-middle fs-1">屋内</span>
            </button>
            <button type="button" id="1" name="movePageTo" class="btn btn-outline-success btn-lg">
                <span class="material-icons align-middle fs-1 me-1 mb-1">park</span><span class="align-middle fs-1">屋外</span>
            </button>
            <button type="button" id="2" name="movePageTo" class="btn btn-outline-success btn-lg">
                <span class="material-icons align-middle fs-1 me-1 mb-1">watch_later</span><span class="align-middle fs-1">時計</span>
            </button>
            <button type="button" id="3" name="movePageTo" class="btn btn-outline-success btn-lg">
                <span class="material-icons align-middle fs-1 me-1 mb-1">info</span><span class="align-middle fs-1">情報</span>
            </button>
        </div>
        </div></div></div>
        <div class="toast-container position-absolute mt-3 top-50 start-50 translate-middle">
            <div id="toast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header">
                    <svg class="bd-placeholder-img rounded me-2" width="20" height="20" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" role="img" focusable="false"><rect fill="#007aff" width="100%" height="100%"></rect></svg>
                    <strong class="me-auto">Success</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="閉じる"></button>
                </div>
                <div class="toast-body">
                    <h3 class="text-center mb-0">Display switched!</h3>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''
