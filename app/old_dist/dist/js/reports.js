var task_id = null;

function checkStatus(taskId) {
    $.getJSON(`${window.location.protocol}//${window.location.host}/reports/task/${taskId}`, function(data) {
        if (data.status == "SUCCESS") {
            if (data.error) {
                $('#report_modal_content').html(
                    `<div class="overlay-wrapper">
                        <div class="overlay">
                        <p>Ошибка при формировании документа</p>
                        <p>${data.error}</p>
                        </div>
                    </div>`
                );
                return;
            } else {
                console.log(data);
                $('#report_modal_content').html(
                    `<div class="overlay-wrapper">
                        <div class="overlay">
                            <div class="text-bold pt-2">Документы сформированы</div>
                            <div class="text-bold pt-2">Скачать документ:</div>
                            <div class="text-bold pt-2">
                                ${data.files.map(function(file) {
                                    return `<a href="${window.location.protocol}//${window.location.host}${file.url}">${file.name}</a>`;
                                }
                                ).join(' ')}
                            </div>
                        </div>
                    </div>`
                );
            }
        } else if (data.status == "FAILURE") {
            $('#report_modal_content').html(
                `<div class="overlay-wrapper">
                    <div class="overlay">
                    <p>Ошибка при формировании документа</p>
                    </div>
                </div>`
            );
        } else {
            setTimeout(function() {
                checkStatus(taskId);
            }, 500);
        }
    });
}


function sendRequestToURL(url) {
    $.get(
        url,
        function(data) {
        task_id = data.task_id;
        $('#report_modal_content').html(
            `<div class="overlay-wrapper">
                <div class="overlay">
                    <div><i class="fas fa-3x fa-sync-alt fa-spin"></i></div>
                    <div class="text-bold pt-2">Загрузка...</div>
                </div>
            </div>`
        );
        $('#report_modal').modal('show');
        checkStatus(task_id);
        }
    );
};
