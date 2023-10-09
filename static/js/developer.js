$(function () {
    addListener();

    const jacketURL = $("#music-jacket");
    const jacketCheckButton = $("#url-check-button");
    const jacketCheck = $("#jacket-check");
    const testButton = $("#test-button");

    jacketCheckButton.on("click", function() {
        jacketCheck.attr("src", jacketURL.val());
    });

    testButton.on("click", function () {
        checkAllNotNull();
    });
});

function addListener() {
    let elements = [];

    elements[0]  = $("#music-id");
    elements[1]  = $("#music-title");
    elements[2]  = $("#music-ruby");
    elements[3]  = $("#music-artist");
    elements[4]  = $("#music-genre");
    elements[5]  = $("#music-version");
    elements[6]  = $("#music-bpm");
    elements[7]  = $("#music-jacket");
    elements[8]  = $("#basic-const");
    elements[9]  = $("#advanced-const");
    elements[10] = $("#expert-const");
    elements[11] = $("#master-const");
    elements[12] = $("#ultima-const");
    elements[13] = $("#expert-nd");
    elements[14] = $("#master-nd");
    elements[15] = $("#ultima-nd");

    for (let i = 0; i < elements.length; i++) {
        elements[i].on("input", checkAllNotNull);
        elements[i].on("change", checkAllNotNull);
    }
}

function checkAllNotNull() {
    const addButton = $("#music-add-button");
    let booleans = [];

    booleans[0]  = $("#music-id").val();
    booleans[1]  = $("#music-title").val();
    booleans[2]  = $("#music-ruby").val();
    booleans[3]  = $("#music-artist").val();
    booleans[4]  = $("#music-genre").val();
    booleans[5]  = $("#music-version").val();
    booleans[6]  = $("#music-bpm").val();
    booleans[7]  = $("#music-jacket").val();
    booleans[8]  = $("#basic-const").val();
    booleans[9]  = $("#advanced-const").val();
    booleans[10] = $("#expert-const").val();
    booleans[11] = $("#master-const").val();
    booleans[12] = $("#ultima-const").val();
    booleans[13] = $("#expert-nd").val();
    booleans[14] = $("#master-nd").val();
    booleans[15] = $("#ultima-nd").val();

    for (let i = 0; i < booleans.length; i++) {
        if (booleans[i].length <= 0) {
            addButton.addClass("disabled");
            return;
        }
    }

    addButton.removeClass("disabled");
}