saveBtn = document.querySelector('#save')
addBtn = document.querySelector('#add')
submitBtn = document.querySelector('#submit')
form = document.querySelector('form')

let q_number = 2

saveBtn.onclick = () => {
    submitBtn.click()
}

addBtn.onclick = () => {
    quiz = document.createElement('div')
    quiz.classList.add("quiz-form__quiz")

    label = document.createElement('label')
    label.setAttribute('for', `q_${q_number}`)
    label.innerHTML = `${q_number}.`

    q_inp = document.createElement('input')
    q_inp.type = 'text'
    q_inp.name = `q_${q_number}`
    q_inp.id = `q_${q_number}`
    q_inp.classList.add('quiz-form__question')
    q_inp.required = true

    quiz.appendChild(label)
    quiz.appendChild(q_inp)

    for (let i = 1; i < 4 + 1; i++) {
        div = document.createElement('div')
        div.classList.add('quiz-form__ans')

        r_inp = document.createElement('input')
        r_inp.type = 'radio'
        // r_inp.id = `${q_number}_choice_${i}`
        r_inp.name = `${q_number}_radio_option`
        r_inp.value = i
        r_inp.required = true

        span = document.createElement('span')
        span.classList.add('design')

        o_inp = document.createElement('input')
        o_inp.type = 'text'
        o_inp.name = `${q_number}_option${i}`
        o_inp.placeholder = `Option ${i}`
        o_inp.required = true

        div.appendChild(r_inp)
        div.appendChild(span)
        div.appendChild(o_inp)
        quiz.appendChild(div)
    }

    footer = document.createElement('div')
    footer.classList.add('footer')

    point = document.createElement('div')
    point.classList.add('point')

    inp = document.createElement('input')
    inp.type = 'number'
    inp.name = `${q_number}_point`
    inp.value = 1
    inp.required = true
    inp.min = 0

    span = document.createElement('span')
    span.innerHTML = 'points'

    point.appendChild(inp)
    point.appendChild(span)
    footer.appendChild(point)
    quiz.appendChild(footer)

    form.appendChild(quiz)

    q_number++

    q_inp.focus()
    quiz.scrollIntoView();
}