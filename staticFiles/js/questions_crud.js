$(document).ready(function () {
    console.log("📘 Question JS Loaded");

    // 🔁 Load Subjects based on Category (with .off().on() to avoid duplicates)
    $("#category").off("change").on("change", function () {    //.off().on() ensures no duplicate handlers are attached if the script runs multiple times.
        const categoryId = $(this).val();
        $("#subject").html('<option value="">Loading...</option>');
        $("#set").html('<option value="">-- Select Set --</option>');

        if (!categoryId) {
            $("#subject").html('<option value="">-- Select Subject --</option>');
            $("#set").html('<option value="">-- Select Set --</option>');
            return;
        }

        $.get(`/questions/get_subjects/${categoryId}/`, function (data) {
            let options = '<option value="">-- Select Subject --</option>';
            data.subjects.forEach(subject => {
                options += `<option value="${subject.id}">${subject.name}</option>`;
            });
            $("#subject").html(options);
        }).fail(function () {
            $("#subject").html('<option value="">Failed to load subjects</option>');
        });
    });

    // 🔁 Load Sets based on Subject (no change needed here, but .off().on() is good practice)
    $("#subject").off("change").on("change", function () {
        const subjectId = $(this).val();
        $("#set").html('<option value="">Loading...</option>');

        if (!subjectId) {
            $("#set").html('<option value="">-- Select Set --</option>');
            return;
        }

        $.get(`/questions/get_sets/${subjectId}/`, function (data) {
            let options = '<option value="">-- Select Set --</option>';
            data.sets.forEach(set => {
                options += `<option value="${set.id}">${set.name}</option>`;
            });
            $("#set").html(options);
        }).fail(function () {
            $("#set").html('<option value="">Failed to load sets</option>');
        });
    });

    // 🔁 Submit Question Form (Add/Edit)
    $("#add-question-form").submit(function (e) {
        e.preventDefault();
        const formData = $(this).serialize();
        const questionId = $("#question_id").val();
        const url = questionId ? `/questions/edit/${questionId}/` : `/questions/add/`;

        $.ajax({
            type: "POST",
            url: url,
            data: formData,
            success: function (response) {
                $("#acknowledge").text(response.message)
                    .css("color", "green").fadeIn().delay(2000).fadeOut();

                // Reset form
                $("#add-question-form")[0].reset();
                $("#question_id").val("");
                $("#add-question-btn").text("Add Question");

                // Refresh rows conditionally
                if ($("#question-table-body").length) {
                    $("#question-table-body").html(response.html);
                } else if ($("#question-rows").length) {
                    $("#question-rows").html(response.html);
                }

                $(".error-message").empty();
            },
            error: function (xhr) {
                const errors = xhr.responseJSON;
                $(".text-danger").html("");
                for (const field in errors) {
                    $(`#error-${field}`).html(errors[field]);
                }
            }
        });
    });

    // 🔄 Submit CSV Question Upload Form
    $("#upload-question-form").submit(function (e) {
        e.preventDefault();

        let formData = new FormData(this);
        const questionId = $("#question_id").val();
        const url = questionId ? `/questions/edit/${questionId}/` : `/questions/upload-questions/`;

        $.ajax({
            type: "POST",
            url: url,
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $("#acknowledge").text(response.message)
                    .css("color", "green").fadeIn().delay(2000).fadeOut();

                $("#upload-question-form")[0].reset();
                $("#question_id").val("");

                $("#question-table-body").html(response.html);

                $(".error-message").empty();
            },
            error: function (xhr) {
                const errors = xhr.responseJSON || {};
                $(".error-message").empty();
                for (const field in errors) {
                    $(`#error-${field}`).html(errors[field]);
                }
            }
        });
    });

    // 🔁 Delete Question (with CSRF token)
    $(document).off("click", ".delete-question").on("click", ".delete-question", function () {
        const questionId = $(this).data("id");
        const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        if (!confirm("AJAX: Are you sure you want to delete this question?")) return;

        $.ajax({
            url: `/questions/delete/${questionId}/`,
            method: "POST",
            data: { csrfmiddlewaretoken: csrfToken },
            success: function (response) {
                $("#acknowledge").text(response.message || "Question deleted successfully!")
                    .css("color", "green").fadeIn().delay(2000).fadeOut();

                if ($("#question-table-body").length) {
                    $("#question-table-body").html(response.html);
                } else if ($("#question-rows").length) {
                    $("#question-rows").html(response.html);
                }
            },
            error: function (xhr) {
                $("#acknowledge").text(xhr.responseJSON?.message || "Failed to delete the question.")
                    .css("color", "red").fadeIn().delay(2000).fadeOut();
            }
        });
    });

    // 🔁 Edit Question - Fill form with data
    $(document).off("click", ".edit-question").on("click", ".edit-question", function () {
        const questionId = $(this).data("id");
        const questionText = $(this).data("question");
        const categoryId = $(this).data("category");
        const subjectId = $(this).data("subject");
        const setId = $(this).data("set");
        const optionA = $(this).data("a");
        const optionB = $(this).data("b");
        const optionC = $(this).data("c");
        const optionD = $(this).data("d");
        const correct = $(this).data("correct");

        // Set initial values
        $("#question_id").val(questionId);
        $("#question_text").val(questionText);
        $("#option_a").val(optionA);
        $("#option_b").val(optionB);
        $("#option_c").val(optionC);
        $("#option_d").val(optionD);
        $("#correct_option").val(correct);

        $("#category").val(categoryId);
        $("#add-question-btn").text("Update Question");

        // Fetch Subjects and Sets and set selected
        $.get(`/questions/get_subjects/${categoryId}/`, function (data) {
            let subjectOptions = '<option value="">-- Select Subject --</option>';
            data.subjects.forEach(subject => {
                subjectOptions += `<option value="${subject.id}" ${subject.id == subjectId ? "selected" : ""}>${subject.name}</option>`;
            });
            $("#subject").html(subjectOptions);

            $.get(`/questions/get_sets/${subjectId}/`, function (data2) {
                let setOptions = '<option value="">-- Select Set --</option>';
                data2.sets.forEach(set => {
                    setOptions += `<option value="${set.id}" ${set.id == setId ? "selected" : ""}>${set.name}</option>`;
                });
                $("#set").html(setOptions);
            });
        });
    });

    // 🔁 Restore Question
    $(document).off("click", ".restore-question-btn").on("click", ".restore-question-btn", function () {
        const id = $(this).data("id");
        const csrfToken = $("#csrf-form input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: `/questions/restore/${id}/`,
            type: "POST",
            headers: { "X-CSRFToken": csrfToken },
            success: function (response) {
                alert(response.message);
                location.reload();
            },
            error: function (xhr) {
                alert(xhr.responseJSON?.message || "Failed to restore question.");
            }
        });
    });

});
