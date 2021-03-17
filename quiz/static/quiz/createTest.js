saveBtn = document.querySelector('#save')
addBtn = document.querySelector('#add')
form = document.querySelector('form')

let q_number = 2

saveBtn.onclick = () => form.submit()


addBtn.onclick = () => {
    formDiv = document.createElement('div')

    questionDiv = document.createElement('div')
    questionDiv.classList.add("question")

    label = document.createElement('label')
    label.setAttribute('for', 'question')
    label.innerHTML = `${q_number}.`

    inp = document.createElement('input')
    inp.type = 'text'
    inp.name = `q_${q_number}`
    inp.id = `q_${q_number}`

    questionDiv.appendChild(label)
    questionDiv.appendChild(inp)

    optionsDiv = document.createElement('div')
    optionsDiv.classList.add('options')

    for (let i = 1; i < 4 + 1; i++) {
        optionDiv = document.createElement('div')
        optionDiv.classList.add('option')

        r_inp = document.createElement('input')
        r_inp.type = 'radio'
        r_inp.id = `${q_number}_option${i}`
        r_inp.name = `${q_number}_radio_option`
        r_inp.value = i

        o_inp = document.createElement('input')
        o_inp.type = 'text'
        o_inp.name = `${q_number}_option${i}`
        o_inp.placeholder = `Option ${i}`

        optionDiv.appendChild(r_inp)
        optionDiv.appendChild(o_inp)
        optionsDiv.appendChild(optionDiv)
    }

    formDiv.append(questionDiv)
    formDiv.append(optionsDiv)
    form.appendChild(formDiv)

    q_number++
}

// < script type = "text/javascript" >
//     window.addEventListener('DOMContentLoaded', () => {
//         console.log('script')
//         saveBtn = document.querySelector('#save')
//         addBtn = document.querySelector('#add')
//         form = `{% include 'create_test/question.html' %}`
//         form = '<h1> Hello </h1>'
//         addBtn.addEventListener('click', () => {
//             console.log('add')
//             document.body.innerHTML += form
//         })

//         saveBtn.onclick = () => {
//             console.log('save')
//         }
//     })
// </script > 