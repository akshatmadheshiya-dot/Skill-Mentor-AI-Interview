setTimeout(() => {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        flash.style.opacity = '0';
        setTimeout(() => flash.remove(), 300);
    });
}, 5000);

/*let timeLeft = 60;
let timerInterval;

function startTimer() {
    timeLeft = 60; // reset for each question
    document.getElementById('time-left').textContent = timeLeft;
    timerInterval = setInterval(updateTimer, 1000);
}

function updateTimer() {
    timeLeft--;
    document.getElementById('time-left').textContent = timeLeft;
    if (timeLeft <= 0) {
        clearInterval(timerInterval);
        submitAnswer(); // auto-submit when time runs out
    }
}*/

document.getElementById('submit-answer')?.addEventListener('click', function() {
    submitAnswer();
});

function submitAnswer() {
    clearInterval(timerInterval);
    const answerInput = document.getElementById('answer');
    const answer = answerInput ? answerInput.value : '';

    fetch('/next_question', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ answer: answer })
    })
    .then(response => response.json())
    .then(data => {
        if (data.completed) {
            alert(data.feedback);
            window.location.href = '/results';
        } else {
            // Load next question
            document.getElementById('question-text').textContent = data.question;
            if(answerInput) answerInput.value = '';
         //   startTimer(); // restart timer for next question
        }
    });
}

// Automatically start timer if interview page exists
/*if(document.getElementById('time-left')) {
    startTimer();
}*/

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const navMenu = document.getElementById('nav-menu');

    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            navMenu.classList.toggle('show-mobile-menu');
        });

        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('show-mobile-menu');
            });
        });

        document.addEventListener('click', (event) => {
            const clickedInside = mobileMenuBtn.contains(event.target) || navMenu.contains(event.target);
            if (!clickedInside && navMenu.classList.contains('show-mobile-menu')) {
                navMenu.classList.remove('show-mobile-menu');
            }
        });

        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                navMenu.classList.remove('show-mobile-menu');
            }
        });
    }
});