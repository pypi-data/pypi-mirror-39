function elcatoSearchInit(path, data) {
    M.AutoInit();
    document.addEventListener("DOMContentLoaded", function() {
        var elcatoSearchElement = document.querySelector("#search");
        function searchGo(item) {
            window.location.href = path + "posts/" + data[item] + ".html";
        }

        var elcatoSearch = M.Autocomplete.init(elcatoSearchElement, {
            minLength: 1,
            onAutocomplete: searchGo,
        });
        elcatoSearch.updateData(data);
    });
}
