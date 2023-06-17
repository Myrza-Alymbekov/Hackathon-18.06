const deleteBtns = document.querySelectorAll('a[data-target="#tunduk-delete"]')
const tundukForm = document.getElementById("tunduk_delete")

function changeUrl(url, attr1, attr2) {
    const url_mask = url.replace(`/${attr1}/`, `/${attr2}/`);
    return url_mask;
}

deleteBtns.forEach(deleteBtn => {
    deleteBtn.addEventListener('click', function(e) {
    const regex = /\d+/g
    let newId = e.target.closest('tr').getElementsByTagName('td')[1].textContent
    const tundukFormAction = tundukForm.getAttribute('action')
    const previousId = tundukFormAction.match(regex)[1]
    tundukForm.setAttribute('action', changeUrl(tundukFormAction, previousId, newId))
})
})


