$(function() {
    // ページネーションボタンがクリックされたときの処理
    $(".page-item").on("click", function(e) {
        // e.preventDefault();

        // 選択されたページのデータを非同期で読み込み
        let pageId = Number($(this).attr("id").replace("page-", ""));

        $.ajax({
            url: "/get-musics?p=" + pageId, // サーバーからデータを取得するエンドポイント
            type: "GET",
            dataType: "json"
        }).done(function(data) {
            // データをテーブルに反映
            let tbody = $("#musics-table tbody");
            tbody.empty(); // 既存のデータをクリア

            for (let i = 1; i <= 13; i++) {
                const link = $(`#page-${i}`);

                if (i === pageId) {
                    link.addClass("active");
                } else {
                    link.removeClass("active");
                }
            }

            for (let i = 0; i < data.length; i++) {
                const row = $(`
                    <tr>
                        <td><img src="${ data[i]['jacket'] }" alt="${ data[i]['title'] }" width="64px" height="64px"></td>
                        <td>${ data[i]['id'] }</td>
                        <td>${ data[i]['title'] }</td>
                        <td>${ data[i]['ruby'] }</td>
                        <td>${ data[i]['artist'] }</td>
                        <td>${ data[i]['genre'] }</td>
                        <td>${ data[i]['version'] }</td>
                        <td>${ data[i]['bpm'] }</td>
                        <td>${ data[i]['basic-const'] }</td>
                        <td>${ data[i]['advanced-const'] }</td>
                        <td>${ data[i]['expert-const'] }</td>
                        <td>${ data[i]['master-const'] }</td>
                        <td>${ data[i]['ultima-const'] }</td>
                        <td>${ data[i]['expert-nd'] }</td>
                        <td>${ data[i]['master-nd'] }</td>
                        <td>${ data[i]['ultima-nd'] }</td>
                        <td style="text-align: center">
                            <a class="btn btn-sm btn-danger" href="/delete-song?id=${data[i]['id']}">
                                <i class="bi-trash3-fill"></i>
                            </a>
                        </td>
                    </tr>
                `);

                tbody.append(row);
            }
        });
    });
});