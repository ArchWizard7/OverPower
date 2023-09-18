$(function () {
    const jacket = $("#music-jacket");
    const uuidGenerate = $("#uuid-generate-button");
    const add = $("#music-add-button");

    $("input, select").on("change", checkNull);

    uuidGenerate.on("click", function () {
        jacket.val(createUuid());
        checkNull();
    });

    add.on("click", function () {
        const id = $("#music-id");
        const title = $("#music-title");
        const ruby = $("#music-ruby");
        const artist = $("#music-artist");
        const genre = $("#music-genre option:selected");
        const version = $("#music-version option:selected");
        const bpm = $("#music-bpm");

        addMusic(id.val(), title.val(), ruby.val(), artist.val(), genre.text(), version.text(), bpm.val(), jacket.val());
    });
});

function createUuid(){
    return '********-****-4***-y***-************'.replace(/[*y]/g, function(a) {
        let r = (new Date().getTime() + Math.random() * 16) % 16 | 0, v = (a === '*') ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

function checkNull() {
    const btn = $("#music-add-button");
    btn.addClass("disabled");

    const array = [
        $("#music-id").val(),
        $("#music-title").val(),
        $("#music-ruby").val(),
        $("#music-artist").val(),
        $("#music-bpm").val(),
    ]

    for (let i in array) {
        if (array[i].length === 0) return;
    }

    if ($("#music-genre").val().startsWith("Choose")) return;
    if ($("#music-version").val().startsWith("Choose")) return;

    const regex = new RegExp("([0-9a-f]{8})-([0-9a-f]{4})-(4[0-9a-f]{3})-([0-9a-f]{4})-([0-9a-f]{12})");
    if (regex.test($("#music-jacket").val())) {
        btn.removeClass("disabled");
    }
}

function addMusic(id, title, ruby, artist, genre, version, bpm, jacket) {
    const array = {
        id: id,
        title: title,
        ruby: ruby,
        artist: artist,
        genre: genre,
        version: version,
        bpm: bpm,
        jacket: jacket
    }

    $.ajax({
        method: "POST",
        url: "/add-music",
        data: JSON.stringify(array),
        contentType: "application/json"
    }).done(function (data) {
        console.log(JSON.stringify(data));
        const alert = $("#music-alert");
        alert.css("display", "inline");
        alert.removeClass("alert-danger");
        alert.addClass("alert-success");
        alert.html(`
                <i class="bi-check-circle-fill"></i>
                楽曲の追加に成功しました
            `);
    }).fail(function (error) {
        const alert = $("#music-alert");
        alert.css("display", "inline");
        alert.removeClass("alert-success");
        alert.addClass("alert-danger");
        alert.html(`
                <i class="bi-x-square-fill"></i>
                楽曲の追加に失敗しました
            `);
    });
}