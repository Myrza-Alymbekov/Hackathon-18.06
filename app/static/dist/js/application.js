// {#Variable for pagination#}
const paginationNumbers = document.getElementById("pagination-numbers");
const paginatedList = document.getElementById("paginated-list");
const listItems = paginatedList.querySelectorAll(".pagination__comments");
const nextButton = document.getElementById("next-button");
const prevButton = document.getElementById("prev-button");
const paginationLimit = 3;
const pageCount = Math.ceil(listItems.length / paginationLimit);
let currentPage = 1;
// {#Variable for tranch#}
const sumTranche = document.getElementById('id_sum_tranche')
const period = document.getElementById('id_period')
const checkbox = document.getElementById('id_is_tranche')
const sumTrancheLabel = document.querySelector('label[for="id_sum_tranche"]')
const periodLabel = document.querySelector('label[for="id_period"]')
// {#Variable for deleting guarantor and pledger#}
const table = document.getElementsByClassName("table");
const actions = document.querySelectorAll('.pledger_gurantor__actions')

// {#Script for paginated#}
const disableButton = (button) => {
    button.classList.add("disabled");
    button.setAttribute("disabled", true);
};

const enableButton = (button) => {
    button.classList.remove("disabled");
    button.removeAttribute("disabled");
};

const handlePageButtonsStatus = () => {
    if (currentPage === 1) {
        disableButton(prevButton);
    } else {
        enableButton(prevButton);
    }

    if (pageCount === currentPage) {
        disableButton(nextButton);
    } else {
        enableButton(nextButton);
    }
};

const handleActivePageNumber = () => {
    document.querySelectorAll(".pagination-number").forEach((button) => {
        button.classList.remove("active");
        const pageIndex = Number(button.getAttribute("page-index"));
        if (pageIndex == currentPage) {
            button.classList.add("active");
        }
    });
};

const appendPageNumber = (index) => {
    const pageNumber = document.createElement("button");
    pageNumber.className = "pagination-number";
    pageNumber.innerHTML = index;
    pageNumber.setAttribute("page-index", index);
    pageNumber.setAttribute("aria-label", "Page " + index);

    paginationNumbers.appendChild(pageNumber);
};

const getPaginationNumbers = () => {
    for (let i = 1; i <= pageCount; i++) {
        appendPageNumber(i);
    }
};

const setCurrentPage = (pageNum) => {
    currentPage = pageNum;

    handleActivePageNumber();
    handlePageButtonsStatus();

    const prevRange = (pageNum - 1) * paginationLimit;
    const currRange = pageNum * paginationLimit;

    listItems.forEach((item, index) => {
        item.classList.add("hidden");
        if (index >= prevRange && index < currRange) {
            item.classList.remove("hidden");
        }
    });
};

window.addEventListener("load", () => {
    getPaginationNumbers();
    setCurrentPage(1);

    prevButton.addEventListener("click", () => {
        setCurrentPage(currentPage - 1);
    });

    nextButton.addEventListener("click", () => {
        setCurrentPage(currentPage + 1);
    });

    document.querySelectorAll(".pagination-number").forEach((button) => {
        const pageIndex = Number(button.getAttribute("page-index"));

        if (pageIndex) {
            button.addEventListener("click", () => {
                setCurrentPage(pageIndex);
            });
        }
    });
});

// {#Script for deleting guarantor and pledger#}

function changeUrl(url, attr1, attr2) {
    const url_mask = url.replace(attr1, attr2);
    return url_mask;
}

function changeUrlGuarantorAndPledgerModal(formClass, e) {
    let newId = e.target.closest('tr').firstElementChild.textContent
    const form = document.querySelector(formClass)
    const formAction = form.getAttribute("action")
    const previousId = formAction.match(/\d+/)[0]
    form.setAttribute('action', changeUrl(formAction, previousId, newId))
}

actions.forEach(function (action) {
    action.addEventListener('click', function (e) {
        if (e.target.classList.contains('fa-trash')) {
            if (this.children.item(1).getAttribute('data-target') === '#pledger-delete') {
                changeUrlGuarantorAndPledgerModal('.pledger__form', e)
            } else if (this.children.item(1).getAttribute('data-target') === '#guarantor-delete') {
                changeUrlGuarantorAndPledgerModal('.gurantor__form', e)
            }
        }
    })
})

// {#Script for tranch#}
checkbox.style.cssText = "height: 20px; width: 20px;"
sumTranche.setAttribute('hidden', '')
period.setAttribute('hidden', '')
sumTrancheLabel.setAttribute('hidden', '')
periodLabel.setAttribute('hidden', '')
checkbox.addEventListener('click', () => {

    if (checkbox.checked === true) {
        sumTrancheLabel.removeAttribute('hidden')
        periodLabel.removeAttribute('hidden')
        sumTranche.removeAttribute('hidden')
        period.removeAttribute('hidden')
    }
    if (checkbox.checked === false) {
        periodLabel.setAttribute('hidden', '')
        sumTrancheLabel.setAttribute('hidden', '')
        sumTranche.setAttribute('hidden', '')
        period.setAttribute('hidden', '')
    }
})