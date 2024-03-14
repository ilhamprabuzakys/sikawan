/**  ===============
    MAIN - DASHBOARD
==================== **/
$(function () {
    moment.locale('id');
    new PureCounter({
        selector: '.purecounter'
    });

    expandBodyLength();
});

function fetchSearchResults() {
    console.log('Searching a page with query :', this.searchInput);

    var role = document.getElementById('global_search_input').getAttribute('data-role');
    var url = `/static/data/pages/${role}_pages.json`;

    if (this.searchInput.length > 0) {
        axios.get(url)
            .then(response => {
                this.searchResults = response.data.pages.filter(page =>
                    page.name.toLowerCase().includes(this.searchInput.toLowerCase())
                );
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    } else {
        this.searchResults = [];
    }
}


// function handleSearch(val) {
//     console.log('Searching a page with query :', val)

//     var role = $('#global_search_input').data('role');
//     var url = `/static/data/pages/${role}_pages.json`;

//     if (val.length > 0) {
//         axios.get(url)
//             .then(function (response) {
//                 var pages = response.data.pages;
//                 var searchResults = pages.filter(function (page) {
//                     return page.name.toLowerCase().includes(val.toLowerCase());
//                 });
//                 displaySearchResults(searchResults);
//             })
//             .catch(function (error) {
//                 console.error('Error fetching data:', error);
//             });
//     } else {
//         $('#global_search_results').empty();
//     }
// }

// function displaySearchResults(results) {
//     let resultList = $('#global_search_results');
//     resultList.empty();
//     if (results.length > 0) {
//         results.forEach(function (result) {
//             let el = `
//                 <a href="${result.url}" class="list-group-item list-group-item-action" x-on:click.stop>
//                     <i class="${result.icon} me-2"></i>${result.name}
//                 </a>
//             `;

//             resultList.append(el);
//         });
//     } else {
//         let message = `Tidak ada hasil ditemukan`;
//         let el = `
//                 <a href="javascript:void(0);" class="list-group-item list-group-item-action disabled" x-on:click.stop>
//                     ${message}
//                 </a>
//             `;

//         resultList.append(el);
//     }
// }

function expandBodyLength() {
    $("#layout-navbar").addClass("container-fluid").removeClass("container-xxl");
    $("#main-content").addClass("container-fluid").removeClass("container-xxl");
}

// Handle filter
$('#resetFilter, #applyFilter').on('click', function () {
    $(this).closest('.dropdown-menu').prev('.dropdown-toggle').dropdown('toggle');
});