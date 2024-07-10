

const BASE = `${location.origin}/api/vacancy/`;

let vacancyForm = document.getElementById('VacancyForm');
let alertArea = document.getElementById('alert')

document.addEventListener('DOMContentLoaded', function () {
    vacancyForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        let formData = new FormData(vacancyForm);
        let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        let response = await fetch(BASE, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData
        });
        if (response.ok) {
            alertArea.innerHTML = ''
            alertArea.innerHTML += `
                <div class="alert alert-success w-100 d-flex justify-content-center align-items-center">
                    <strong>Müraciətiniz göndərildi</strong>
                </div>
            `
        } else {
            let data = await response.json();
            if (data && data.non_field_errors) {
                alertArea.innerHTML = ''
                alertArea.innerHTML += `
                    <div class="alert alert-danger w-100 d-flex justify-content-center align-items-center">
                       <strong>${data.non_field_errors[0]}</strong>
                    </div>
                `
            } else if (data && data.CV) {
                if (data.CV[0].includes('encoding')) {
                    alertArea.innerHTML = ''
                    alertArea.innerHTML += `
                        <div class="alert alert-danger w-100 d-flex justify-content-center align-items-center">
                           <strong>Müraciət zamanı CV göndərmək mütləqdir!!!</strong>
                        </div>
                    `
                } else {
                    alertArea.innerHTML = ''
                    alertArea.innerHTML += `
                        <div class="alert alert-danger w-100 d-flex justify-content-center align-items-center">
                           <strong>CV yalnız pdf və docx formatında göndərilə bilər!!!</strong>
                        </div>
                    `
                }
            } else if (data && data.prtfolio_website) {
                alertArea.innerHTML = ''
                alertArea.innerHTML += `
                    <div class="alert alert-danger w-100 d-flex justify-content-center align-items-center">
                       <strong>Keçərli url daxil edin!!!</strong>
                    </div>
                `
            } else {
                alertArea.innerHTML = ''
                alertArea.innerHTML += `
                    <div class="alert alert-danger w-100 d-flex justify-content-center align-items-center">
                       <strong>Müraciətin göndərilməsində xəta oldu</strong>
                    </div>
                `
            }
        }
        vacancyForm.reset();
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const element = document.querySelector('.animated');
    element.classList.add('animate__animated', 'animate__slideInDown');
    const deadline_animate = document.querySelector('.animated_date');
    deadline_animate.classList.add('animate__animated_date', 'animate__slideInUp');
});