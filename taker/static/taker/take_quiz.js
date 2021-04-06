const form = document.querySelector('form')
const submitBtn = document.querySelector('#submit')
const hiddenBtn = document.querySelector('#hiddenSubmit')
const timeLimitBtn = document.querySelector('#timeLimit')

submitBtn.onclick = () => hiddenBtn.click()

const interval = setInterval(myTimer, 1000)

const endDateTimeUnix = Date.parse(timeLimitBtn.getAttribute('data-endDateTime'))
let timeRemaining = endDateTimeUnix - Date.now()

let seconds = Math.round(timeRemaining / 1000)
let minutes = Math.floor(seconds / 60)
seconds = seconds - minutes * 60

if (seconds < 10) seconds = "0" + seconds
if (seconds <= 20 && minutes == 0) timeLimitBtn.style.background = 'red'
timeLimitBtn.innerHTML = `${minutes}:${seconds}`

function myTimer() {
    seconds--

    if (seconds == -1) {
        minutes--
        seconds = 59
    }

    if (minutes == 0 && seconds == 0) {
        form.submit()
        clearInterval(interval)
    }
    else if (seconds <= 20 && minutes == 0) timeLimitBtn.style.background = 'red'

    if (seconds < 10) seconds = "0" + seconds

    timeLimitBtn.innerHTML = `${minutes}:${seconds}`
}