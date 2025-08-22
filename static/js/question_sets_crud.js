$(document).ready(function () {
    console.log("AJAX Script loaded");

    // Handle Save/Edit Set
    $("#set_register_btn").click(function (event) {
        event.preventDefault();

        const set_id = $("#set_id").val(); // matches HTML
        const set_name = $("#set_name").val();
        const category_id = $("#category").val();
        const subject_id = $("#subject").val();
        const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        if (!set_name || !category_id || !subject_id) {
            $("#acknowledge").text("Set name, category, and subject are required.")
                .css("color", "red").fadeIn().delay(2000).fadeOut();
            return;
        }

        $.ajax({
            url: set_id ? `/question_sets/edit/${set_id}/` : `/question_sets/add/`,
            method: "POST",
            data: {
                set_name: set_name,
                category: category_id,
                subject: subject_id,
                csrfmiddlewaretoken: csrfToken
            },
            success: function (response) {
                $("#set_id").val("");
                $("#set_name").val("");
                $("#category").val("");
                $("#subject").empty().append('<option value="">-- Select Subject --</option>');
                $("h3.text-primary").text("Set Register");
                $("#set_register_btn").text("Save");

                $("#acknowledge").text(response.message || "Set saved successfully!")
                    .css("color", "green").fadeIn().delay(2000).fadeOut();

                $.get("/question_sets/get_rows/", function (data) {
                    $("#setList").html(data.html);
                });
            },
            error: function (error) {
                const errorMessage = error.responseJSON?.message || "An error occurred.";
                $("#acknowledge").text(errorMessage)
                    .css("color", "red").fadeIn().delay(2000).fadeOut();
            }
        });
    });

    // Delete Set
    $(document).on("click", ".delete-set", function () {
        const setId = $(this).data("id");
        const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        if (!confirm("Are you sure?")) return;

        $.ajax({
            url: `/question_sets/delete/${setId}/`,
            method: "POST",
            data: { csrfmiddlewaretoken: csrfToken },
            success: function (response) {
                $("#acknowledge").text(response.message).css("color", "green").fadeIn().delay(2000).fadeOut();
                $.get("/question_sets/get_rows/", function (data) {
                    $("#setList").html(data.html);
                });
            },
            error: function (xhr) {
                $("#acknowledge").text(xhr.responseJSON?.message || "Failed").css("color", "red").fadeIn().delay(2000).fadeOut();
            }
        });
    });

    // Populate Subject dropdown when Category changes
    $("#category").change(function () {
        const categoryId = $(this).val();

        let subjectSelect = $("#subject");
        subjectSelect.empty().append('<option value="">-- Select Subject --</option>');

        if (categoryId) {
            $.ajax({
                url: "/question_sets/get_subjects/",
                method: "GET",
                data: { category_id: categoryId },
                success: function (response) {
                    response.subjects.forEach(subject => {
                        subjectSelect.append(`<option value="${subject.id}">${subject.name}</option>`);
                    });
                },
                error: function (xhr) {
                    console.log("AJAX error:", xhr.status, xhr.responseText);
                }
            });
        }
    });

    // Edit Set
    $(document).on("click", ".edit-set", function () {
        const setId = $(this).data("id");
        const setName = $(this).data("name");
        const categoryId = $(this).data("category");
        const subjectId = $(this).data("subject");

        $("#set_id").val(setId); // corrected ID
        $("#set_name").val(setName);
        $("#category").val(categoryId);
        $("h3.text-primary").text("Edit Set");
        $("#set_register_btn").text("Update");

        // Load subjects for selected category 
        $.ajax({
            url: "/question_sets/get_subjects/",
            method: "GET",
            data: { category_id: categoryId },
            success: function (response) {
                let subjectSelect = $("#subject");
                subjectSelect.empty().append('<option value="">-- Select Subject --</option>');

                response.subjects.forEach(subject => {
                    subjectSelect.append(`<option value="${subject.id}" ${subject.id == subjectId ? 'selected' : ''}>${subject.name}</option>`);
                });
            },
            error: function (xhr) {
                console.log("AJAX error while loading subjects:", xhr.status, xhr.responseText);
            }
        });
    });

    // Restore Set
    $(document).on("click", ".restore-set-btn", function () {
        const id = $(this).data("id");
        const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: `/question_sets/restore/${id}/`,
            type: "POST",
            data: { csrfmiddlewaretoken: csrfToken },
            success: function (response) {
                alert(response.message);
                location.reload();
            },
            error: function (xhr) {
                alert(xhr.responseJSON?.message || "Failed to restore set.");
            }
        });
    });

});
