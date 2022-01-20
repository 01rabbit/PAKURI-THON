// ドラッグ&ドロップエリアの取得
var fileArea = document.getElementById('dropArea');

// input[type=file]の取得
var fileInput = document.getElementById('uploadFile');

// ドラッグオーバー時の処理
fileArea.addEventListener('dragover', function(e) {
    e.preventDefault();
    fileArea.classList.add('dragover');
});

// ドラッグアウト時の処理
fileArea.addEventListener('dragleave', function(e) {
    e.preventDefault();
    fileArea.classList.remove('dragover');
});

// ドロップ時の処理
fileArea.addEventListener('drop', function(e) {
    e.preventDefault();
    fileArea.classList.remove('dragover');

    // ドロップしたファイルの取得
    var files = e.dataTransfer.files;

    // 取得したファイルをinput[type=file]へ
    fileInput.files = files;

    if (typeof files[0] !== 'undefined') {
        //ファイルが正常に受け取れた際の処理
        // .xmlならファイル名を表示
        if (files[0].name.substr(-4) === '.xml') {
            document.getElementById('fileName').innerHTML = files[0].name;
        }
    } else {
        //ファイルが受け取れなかった際の処理
    }
});

// input[type=file]に変更があれば実行
// もちろんドロップ以外でも発火します
fileInput.addEventListener('change', function(e) {
    var file = e.target.files[0];

    if (typeof e.target.files[0] !== 'undefined') {
        // ファイルが正常に受け取れた際の処理
        // .xmlならファイル名を表示
        if (file.name.split('.')[1] === 'xml') {
            document.getElementById('fileName').innerHTML = file.name;
        }
    } else {
        // ファイルが受け取れなかった際の処理
    }
}, false);