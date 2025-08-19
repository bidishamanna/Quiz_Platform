// $(document).ready(function () {
//     let currentSetId = null;
//     let currentQuestionId = null;
//     let score = 0;
//     let totalQuestions = 0;
//     let answeredQuestions = 0;
//     let userAnswers = [];
//     let timer;
//     const QUESTION_TIME = 30; // seconds

//     function startTimer() {
//         let timeLeft = QUESTION_TIME;
//         $('#timer').text(`⏱ ${timeLeft}s`);

//         timer = setInterval(() => {
//             timeLeft--;
//             $('#timer').text(`⏱ ${timeLeft}s`);
//             if (timeLeft <= 0) {
//                 clearInterval(timer);
//                 alert("⏰ Time's up!");
//                 submitAnswer(null);
//             }
//         }, 1000);
//     }

//     function stopTimer() {
//         clearInterval(timer);
//         $('#timer').text('');
//     }

//     $('#start-btn').click(function () {
//         const subjectId = $('#subject-select').val();
//         if (!subjectId) return alert("Please select a subject!");

//         $.get('questions/assign-random-set/', { subject_id: subjectId }, function (data) {
//             if (data.status === 'success') {
//                 currentSetId = data.set_id;
//                 $('#start-btn').hide();
//                 $('#subject-select').prop('disabled', true);
//                 $('#quiz-area').removeClass('d-none');
//                 loadNextQuestion();
//             } else {
//                 alert(data.message);
//             }
//         });
//     });

//     function loadNextQuestion() {
//         $.get('questions/get-question/', { set_id: currentSetId }, function (data) {
//             if (data.status === 'completed') {
//                 stopTimer();
//                 showFinalResult();
//                 return;
//             }

//             stopTimer();
//             currentQuestionId = data.question_id;
//             totalQuestions++;

//             $('#question-box').html(`<h5>${data.text}</h5>`);
//             let optionsHtml = '';
//             $.each(data.options, function (key, value) {
//                 optionsHtml += `
//                     <div class="form-check text-start">
//                         <input class="form-check-input" type="radio" name="option" value="${key}" id="opt${key}">
//                         <label class="form-check-label" for="opt${key}">${key}: ${value}</label>
//                     </div>`;
//             });
//             $('#options-box').html(optionsHtml);
//             startTimer();
//         });
//     }

//     function submitAnswer(selectedOption) {
//         $.post('questions/submit-answer/', {
//             question_id: currentQuestionId,
//             selected_option: selectedOption,
//             csrfmiddlewaretoken: getCSRFToken()
//         }, function (data) {
//             answeredQuestions++;
//             stopTimer();

//             const isCorrect = selectedOption === data.correct_option;
//             if (isCorrect) score++;

//             userAnswers.push({
//                 question: data.question,
//                 selected: selectedOption || 'None',
//                 correct: data.correct_option,
//                 is_correct: isCorrect
//             });

//             loadNextQuestion();
//         });
//     }

//     $('#submit-answer').click(function () {
//         const selectedOption = $('input[name="option"]:checked').val();
//         if (!selectedOption) return alert("Please select an option!");
//         submitAnswer(selectedOption);
//     });

//     function showFinalResult() {
//         let html = `
//             <h4 class="text-success">✅ Test Completed!</h4>
//             <p>Total: ${totalQuestions}</p>
//             <p>Correct: ${score}</p>
//             <p>Wrong: ${totalQuestions - score}</p>
//             <hr><h5>Review:</h5>
//         `;

//         userAnswers.forEach((ans, idx) => {
//             html += `
//                 <div class="text-start mb-3">
//                     <strong>Q${idx + 1}:</strong> ${ans.question}<br>
//                     <span class="text-${ans.is_correct ? 'success' : 'danger'}">
//                         Your Answer: ${ans.selected} | Correct: ${ans.correct}
//                     </span>
//                 </div>`;
//         });

//         $('#quiz-area').html(html);
//     }

//     function getCSRFToken() {
//         return document.cookie
//             .split('; ')
//             .find(row => row.startsWith('csrftoken'))
//             ?.split('=')[1];
//     }
// });

// $(document).ready(function () {
//     let currentSetId = null;
//     let currentAttemptId = null;  // ✅ Track the attempt ID
//     let currentQuestionId = null;
//     let score = 0;
//     let totalQuestions = 0;
//     let userAnswers = [];
//     let timer;
//     const QUESTION_TIME = 30;

//     const subjectId = localStorage.getItem('selectedSubjectId');
//     $('#subject-select').val(subjectId);

//     function startTimer() {
//         let timeLeft = QUESTION_TIME;
//         $('#timer').text(`⏱ ${timeLeft}s`);
//         timer = setInterval(() => {
//             timeLeft--;
//             $('#timer').text(`⏱ ${timeLeft}s`);
//             if (timeLeft <= 0) {
//                 clearInterval(timer);
//                 alert("⏰ Time's up!");
//                 submitAnswer(null);
//             }
//         }, 1000);
//     }

//     function stopTimer() {
//         clearInterval(timer);
//         $('#timer').text('');
//     }
        
//     $('#start-btn').click(function () {
//         if (!subjectId) return alert("Please select a subject!");

//         const token = localStorage.getItem("access_token");

//         $.ajax({
//             url: '/questions/assign-random-set/',
//             type: 'GET',
//             data: { subject_id: subjectId },
//             headers: {
//                 'Authorization': 'Bearer ' + token
//             },
//             success: function (data) {
//                 console.log("Assign Set Response:", data); // ✅ DEBUG

//                 if (data.status === 'success') {
//                     currentSetId = data.set_id;
//                     currentAttemptId = data.attempt_id;

//                     $('#start-btn').hide();
//                     $('#subject-select').prop('disabled', true);
//                     $('#quiz-area').removeClass('d-none');
//                     loadNextQuestion();
//                 } else {
//                     alert(data.message);
//                 }
//             },
//             error: function (xhr) {
//                 console.error("Assignment Error:", xhr.responseText || xhr.statusText);
//                 alert("Authentication failed or unauthorized access.");
//             }
//         });
//     });

//     function loadNextQuestion() {
//         console.log("Loading question for:", {
//             set_id: currentSetId,
//             attempt_id: currentAttemptId
//         });

//         $.ajax({
//             url: '/questions/get-question/',
//             type: 'GET',
//             cache: false,
//             data: {
//                 set_id: currentSetId,
//                 attempt_id: currentAttemptId
//             },
//             success: function (data) {
//                 console.log("Get Question Response:", data); // ✅ DEBUG

//                 if (data.status === 'completed') {
//                     stopTimer();
//                     showFinalResult();
//                     return;
//                 }

//                 stopTimer();
//                 currentQuestionId = data.question_id;
//                 totalQuestions++;

//                 $('#question-box').html(`<h5>${data.text}</h5>`);

//                 let optionsHtml = '';
//                 $.each(data.options, function (key, value) {
//                     optionsHtml += `
//                         <div class="form-check text-start">
//                             <input class="form-check-input" type="radio" name="option" value="${key}" id="opt${key}">
//                             <label class="form-check-label" for="opt${key}">${key}: ${value}</label>
//                         </div>`;
//                 });

//                 $('#options-box').html(optionsHtml);
//                 startTimer();
//             },
//             error: function (xhr) {
//                 console.error("Question Load Error:", xhr.responseText || xhr.statusText);
//                 alert("Failed to load question.");
//             }
//         });
//     }

//     $('#submit-btn').click(function () {
//     const selectedOption = $('input[name="option"]:checked').val();
//     if (!selectedOption) return alert("Please select an option!");

//     submitAnswer(selectedOption);
//     });

//     function submitAnswer(selectedOption) {
//         const token = localStorage.getItem("access_token");

//         $.ajax({
//             url: '/questions/submit-answer/',
//             type: 'POST',
//             headers: {
//                 'Authorization': 'Bearer ' + token,   // ✅ Required for @jwt_required
//                 'X-CSRFToken': getCSRFToken()
//             },
//             data: {
//                 question_id: currentQuestionId,       // ✅ Must be set in your JS
//                 selected_option: selectedOption,      // ✅ Matches backend
//                 attempt_id: currentAttemptId          // ✅ Also must be set
//             },
//             success: function (data) {
//                 const correct = data.correct_option;
//                 const isCorrect = selectedOption === correct;
//                 score += isCorrect ? 1 : 0;

//                 userAnswers.push({
//                     question: data.question,
//                     selected: selectedOption,
//                     correct: correct,
//                     is_correct: isCorrect
//                 });

//                 loadNextQuestion(); // Move to the next question
//             },
//             error: function (xhr) {
//                 console.error("Submit error:", xhr.responseText || xhr.statusText);
//                 alert("Could not submit answer.");
//             }
//         });
//     }

//     function getCSRFToken() {
//         return document.cookie
//             .split('; ')
//             .find(row => row.startsWith('csrftoken'))
//             ?.split('=')[1];
//     }
// })

$(document).ready(function () {
    let currentSetId = null;
    let currentAttemptId = null;
    let currentQuestionId = null;
    let score = 0;
    let totalQuestions = 0;
    let userAnswers = [];
    let timer;
    const QUESTION_TIME = 30;

    const subjectId = localStorage.getItem('selectedSubjectId');

    $('#subject-select').val(subjectId);


    function startTimer() {
        let timeLeft = QUESTION_TIME;
        $('#timer').text(`⏱ ${timeLeft}s`);
        timer = setInterval(() => {
            timeLeft--;
            $('#timer').text(`⏱ ${timeLeft}s`);
            if (timeLeft <= 0) {
                clearInterval(timer);
                // Instead of alert, automatically submit with null
                submitAnswer(null);
            }
        }, 1000);
    }


    function stopTimer() {
        clearInterval(timer);
        $('#timer').text('');
    }

    $('#start-btn').click(function () {
        if (!subjectId) return alert("Please select a subject!");

        const token = localStorage.getItem("access_token");
        // Hide the entire start section (which contains the vertical height spacing)
        $('#start-section').addClass('d-none');

        // Show the quiz area
        $('#quiz-area').removeClass('d-none');

        // OPTIONAL: Scroll to top to ensure quiz is visible immediately
        $('html, body').animate({ scrollTop: $('#quiz-area').offset().top }, 500);

        $.ajax({
            url: '/questions/assign-random-set/',
            type: 'GET',
            data: { subject_id: subjectId },
            
            success: function (data) {
                if (data.status === 'success') {
                    currentSetId = data.set_id;
                    currentAttemptId = data.attempt_id;

                    $('#start-btn').hide();
                    $('#subject-select').prop('disabled', true);
                    $('#quiz-area').removeClass('d-none');
                    loadNextQuestion();
                } else {
                    alert(data.message);
                }
            },
            error: function (xhr) {
                console.error("Assignment Error:", xhr.responseText || xhr.statusText);
                alert("Authentication failed or unauthorized access.");
            }
        });
    });

    function loadNextQuestion() {
        $.ajax({
            url: '/questions/get-question/',
            type: 'GET',
            cache: false,
            data: {
                set_id: currentSetId,
                attempt_id: currentAttemptId
            },
            success: function (data) {
                if (data.status === 'completed') {
                    stopTimer();
                    showFinalResult();
                    return;
                }

                stopTimer();
                currentQuestionId = data.question_id;
                totalQuestions++;

                $('#question-box').html(`
                    <h5 class="text-white text-center mb-4">
                        Question ${totalQuestions}: ${data.text}
                    </h5>
                `);

                let optionsHtml = '';
                $.each(data.options, function (key, value) {
                    optionsHtml += `
                        <div class="form-check text-white text-start mx-auto" style="max-width: 600px;">
                            <input class="form-check-input" type="radio" name="option" value="${key}" id="opt${key}">
                            <label class="form-check-label" for="opt${key}">${key}: ${value}</label>
                        </div>`;
                });

                $('#options-box').html(optionsHtml);
                startTimer();
            },
            error: function (xhr) {
                console.error("Question Load Error:", xhr.responseText || xhr.statusText);
                alert("Failed to load question.");
            }
        });
    }

    $('#submit-btn').click(function () {
        const selectedOption = $('input[name="option"]:checked').val();
        if (!selectedOption) return alert("Please select an option!");
        submitAnswer(selectedOption);
    });

    function submitAnswer(selectedOption) {
         // ✅ grab CSRF token from hidden input rendered by {% csrf_token %}
        const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: '/questions/submit-answer/',
            type: 'POST',
            
            data: {
            question_id: currentQuestionId,
            selected_option: selectedOption || "",  // send as empty string if null
            attempt_id: currentAttemptId,
            csrfmiddlewaretoken: csrfToken  
            },

            success: function (data) {
                const correct = data.correct_option;
                const isCorrect = selectedOption === correct;
                score += isCorrect ? 1 : 0;

                userAnswers.push({
                    question: data.question,
                    selected: selectedOption,
                    correct: correct,
                    is_correct: isCorrect
                });

                loadNextQuestion();
            },

            error: function (xhr) {
                console.error("Submit error:", xhr.responseText || xhr.statusText);
                alert("Could not submit answer.");
            }
        });
    }

    function showFinalResult() {
        let html = `
            <div class="text-center text-white">
                <h4 class="text-success">✅ Test Completed!</h4>
                <p>Total Questions: ${totalQuestions}</p>
                <p>Correct Answers: ${score}</p>
                <p>Wrong Answers: ${totalQuestions - score}</p>
                <hr><h5>Review:</h5>
            </div>
        `;

        userAnswers.forEach((ans, idx) => {
            html += `
                <div class="text-start mb-3 text-white">
                    <strong>Q${idx + 1}:</strong> ${ans.question}<br>
                    <span class="text-${ans.is_correct ? 'success' : 'danger'}">
                        Your Answer: ${ans.selected} | Correct: ${ans.correct}
                    </span>
                </div>`;
        });

        $('#quiz-area').html(html);
    }

  
});


