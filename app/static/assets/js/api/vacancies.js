const BASE_URL = `${location.origin}/api/vacancy/`;

document.addEventListener('DOMContentLoaded', function () {
    const modals = document.querySelectorAll('[id^="exampleModal-"]');

    modals.forEach(function(modal) {
        const vacancyId = modal.id.split('-')[1];
        const vacancyForm = document.getElementById(`vacancy-form-${vacancyId}`);
        const alertArea = document.getElementById(`alert-${vacancyId}`);

        vacancyForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            
            let formData = new FormData(vacancyForm);
            let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

            try {
                let response = await fetch(BASE_URL, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                    },
                    body: formData
                });

                if (response.ok) {
                    alertArea.innerHTML = `
                        <div class="alert alert-success w-100 d-flex justify-content-center align-items-center">
                            <strong>Müraciətiniz göndərildi</strong>
                        </div>
                    `;
                } else {
                    let data = await response.json();

                    if (data && data.non_field_errors) {
                        alertArea.innerHTML = `
                            <div class="alert alert-danger w-100 d-flex justify-content-center align-items-center">
                                <strong>${data.non_field_errors[0]}</strong>
                            </div>
                        `;
                    } else if (data && data.CV) {
                        if (data.CV[0].includes('encoding')) {
                            alertArea.innerHTML = `
                                <div class="alert alert-danger w-100 d-flex justify-content-center align-items-center">
                                    <strong>Müraciət zamanı CV göndərmək mütləqdir!!!</strong>
                                </div>
                            `;
                        } else {
                            alertArea.innerHTML = `
                                <div class="alert alert-danger w-100 d-flex justify-content-center align-items-center">
                                    <strong>CV yalnız pdf və docx formatında göndərilə bilər!!!</strong>
                                </div>
                            `;
                        }
                    } else if (data && data.prtfolio_website) {
                        alertArea.innerHTML = `
                            <div class="alert alert-danger w-100 d-flex justify-content-center align-items-center">
                                <strong>Keçərli url daxil edin!!!</strong>
                            </div>
                        `;
                    } else {
                        alertArea.innerHTML = `
                            <div class="alert alert-danger w-100 d-flex justify-content-center align-items-center">
                                <strong>Müraciətin göndərilməsində xəta oldu</strong>
                            </div>
                        `;
                    }
                }
            } catch (error) {
                alertArea.innerHTML = `
                    <div class="alert alert-danger w-100 d-flex justify-content-center align-items-center">
                        <strong>Xəta baş verdi. Zəhmət olmasa yenidən cəhd edin.</strong>
                    </div>
                `;
            }

            vacancyForm.reset();
        });

        const closeButton = modal.querySelector('.close');
        const cancelButton = modal.querySelector('.cancel')

        closeButton.addEventListener('click', function() {
            alertArea.innerHTML = '';
        });

        cancelButton.addEventListener('click', function() {
            alertArea.innerHTML = '';
        });

        window.addEventListener('click', function() {
            alertArea.innerHTML = '';
        })
    });
});

