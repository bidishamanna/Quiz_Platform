// // static/js/category.js
// $(document).ready(function () {
//     console.log("AJAX Script loaded");

    
    
//     // Subject Edit
//     $(document).on("click", ".edit-subject", function () {
//         const subjectId = $(this).data("id");
//         const subjectName = $(this).data("name");
//         const categoryId = $(this).data("category");

//         $("#subject_id").val(subjectId);
//         $("#subject_name").val(subjectName);
//         $("#category").val(categoryId);
//         $("h3.text-primary").text("Edit Subject");
//         $("#subject_register_btn").text("Update");
//     });

//     // Create or Update Subject
//     $("#subject_register_btn").click(function (event) {
//         event.preventDefault();

//         const subject_id = $("#subject_id").val();
//         const category_id = $("#category").val();
//         const subject_name = $("#subject_name").val().trim();
//         const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

//         if (!subject_name || !category_id) {
//             $("#acknowledge").text("Subject name and category are required.")
//                 .css("color", "red")
//                 .fadeIn().delay(2000).fadeOut();
//             return;
//         }

//         $.ajax({
//             url: subject_id ? `/subject/edit/${subject_id}/` : `/subject/add_subject/`,
//             method: "POST",
//             data: {
//                 subject_id: subject_id,
//                 subject_name: subject_name,
//                 category: category_id,
//                 csrfmiddlewaretoken: csrfToken
//             },
//             success: function (response) {
//                 $("#subject_id").val("");
//                 $("#subject_name").val("");
//                 $("#category").val("");
//                 $("h3.text-primary").text("Subject Register");
//                 $("#subject_register_btn").text("Save");

//                 $("#acknowledge").text("Subject saved successfully!")
//                     .css("color", "green")
//                     .fadeIn().delay(2000).fadeOut();

//                 $.get("/subject/get_rows/", function (data) {
//                     $("#subjectList").html(data.html);
//                 });
//             },

//             error: function (error) {
//                 const errorMessage = error.responseJSON?.message || "An error occurred.";
//                 $("#acknowledge").text(errorMessage)
//                     .css("color", "red")
//                     .fadeIn().delay(2000).fadeOut();
//             }
//         });
//     });

//     // Delete Subject via AJAX
//     $(document).on("click", ".delete-subject", function () {
//         const subjectId = $(this).data("id");
//         const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

//         if (!confirm("Are you sure you want to delete this subject?")) return;

//         $.ajax({
//             url: `/subject/delete/${subjectId}/`,
//             method: "POST",
//             data: {
//                 csrfmiddlewaretoken: csrfToken
//             },
//             success: function () {
//                 $("#acknowledge").text("Subject deleted successfully!")
//                     .css("color", "green")
//                     .fadeIn().delay(2000).fadeOut();

//                 $.get("/subject/get_rows/", function (data) {
//                     $("#subjectList").html(data.html);
//                 });
//             },
//             error: function () {
//                 $("#acknowledge").text("Failed to delete the subject.")
//                     .css("color", "red")
//                     .fadeIn().delay(2000).fadeOut();
//             }
//         });
//     });

//     function getCookie(name) {
//         let cookieValue = null;
//         if (document.cookie && document.cookie !== "") {
//             const cookies = document.cookie.split(";");
//             for (let i = 0; i < cookies.length; i++) {
//                 const cookie = cookies[i].trim();
//                 if (cookie.substring(0, name.length + 1) === name + "=") {
//                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                     break;
//                 }
//             }
//         }
//         return cookieValue;
//     }

//     $(document).on("click", ".restore-subject-btn", function () {
//         const id = $(this).data("id");
//         const csrfToken = getCookie("csrftoken");

//         $.ajax({
//             url: `/subject/restore/${id}/`,
//             type: "POST",
//             beforeSend: function (xhr) {
//                 xhr.setRequestHeader("X-CSRFToken", csrfToken);
//             },
//             success: function (response) {
//                 alert(response.message);
//                 location.reload();
//             },
//             error: function (xhr) {
//                 alert(xhr.responseJSON?.message || "Failed to restore subject.");
//             }
//         });
//     });
// })
// static/js/category.js

$(document).ready(function () {
    console.log("AJAX Script loaded");

    // Toggle price field visibility based on requires_payment checkbox
    $("#requires_payment").change(function () {
        if ($(this).is(":checked")) {
            $("#price_group").show();
        } else {
            $("#price_group").hide();
            $("#price").val("");
        }
    });

    // Subject Edit
    $(document).on("click", ".edit-subject", function () {
        const subjectId = $(this).data("id");
        const subjectName = $(this).data("name");
        const categoryId = $(this).data("category");
        const requiresPayment = $(this).data("requires-payment") === true || $(this).data("requires-payment") === "True" || $(this).data("requires-payment") === 1;
        const price = $(this).data("price");

        $("#subject_id").val(subjectId);
        $("#subject_name").val(subjectName);
        $("#category").val(categoryId);

        $("#requires_payment").prop("checked", requiresPayment);

        if (requiresPayment) {
            $("#price_group").show();
            $("#price").val(price);
        } else {
            $("#price_group").hide();
            $("#price").val("");
        }

        $("h3.text-primary").text("Edit Subject");
        $("#subject_register_btn").text("Update");
    });

    // Create or Update Subject
    $("#subject_register_btn").click(function (event) {
        event.preventDefault();

        const subject_id = $("#subject_id").val();
        const category_id = $("#category").val();
        const subject_name = $("#subject_name").val().trim();
        const requires_payment = $("#requires_payment").is(":checked");
        const price = requires_payment ? ($("#price").val() || 0) : 0;
        const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        if (!subject_name || !category_id) {
            $("#acknowledge").text("Subject name and category are required.")
                .css("color", "red")
                .fadeIn().delay(2000).fadeOut();
            return;
        }

        $.ajax({
            url: subject_id ? `/subject/edit/${subject_id}/` : `/subject/add_subject/`,
            method: "POST",
            data: {
                subject_id: subject_id,
                subject_name: subject_name,
                category: category_id,
                requires_payment: requires_payment,
                price: price,
                csrfmiddlewaretoken: csrfToken
            },
            success: function (response) {
                $("#subject_id").val("");
                $("#subject_name").val("");
                $("#category").val("");
                $("#requires_payment").prop("checked", false);
                $("#price").val("");
                $("#price_group").hide();

                $("h3.text-primary").text("Subject Register");
                $("#subject_register_btn").text("Save");

                $("#acknowledge").text("Subject saved successfully!")
                    .css("color", "green")
                    .fadeIn().delay(2000).fadeOut();

                $.get("/subject/get_rows/", function (data) {
                    $("#subjectList").html(data.html);
                });
            },
            error: function (error) {
                const errorMessage = error.responseJSON?.message || "An error occurred.";
                $("#acknowledge").text(errorMessage)
                    .css("color", "red")
                    .fadeIn().delay(2000).fadeOut();
            }
        });
    });

    // Delete Subject via AJAX
    $(document).on("click", ".delete-subject", function () {
        const subjectId = $(this).data("id");
        const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        if (!confirm("Are you sure you want to delete this subject?")) return;

        $.ajax({
            url: `/subject/delete/${subjectId}/`,
            method: "POST",
            data: {
                csrfmiddlewaretoken: csrfToken
            },
            success: function () {
                $("#acknowledge").text("Subject deleted successfully!")
                    .css("color", "green")
                    .fadeIn().delay(2000).fadeOut();

                $.get("/subject/get_rows/", function (data) {
                    $("#subjectList").html(data.html);
                });
            },
            error: function () {
                $("#acknowledge").text("Failed to delete the subject.")
                    .css("color", "red")
                    .fadeIn().delay(2000).fadeOut();
            }
        });
    });

        // Restore Subject
    // Restore Subject
    $(document).on("click", ".restore-subject-btn", function () {
        const id = $(this).data("id");

        // ✅ grab csrf token from hidden input rendered by {% csrf_token %}
        const csrfToken = $("#csrf-form input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: `/subject/restore/${id}/`,
            type: "POST",
            headers: { "X-CSRFToken": csrfToken },  // set CSRF header
            success: function (response) {
                alert(response.message);
                location.reload();
            },
            error: function (xhr) {
                alert(xhr.responseJSON?.message || "Failed to restore subject.");
            }
        });
    });


    // // Helper to get CSRF token
    // function getCookie(name) {
    //     let cookieValue = null;
    //     if (document.cookie && document.cookie !== "") {
    //         const cookies = document.cookie.split(";");
    //         for (let i = 0; i < cookies.length; i++) {
    //             const cookie = cookies[i].trim();
    //             if (cookie.substring(0, name.length + 1) === name + "=") {
    //                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
    //                 break;
    //             }
    //         }
    //     }
    //     return cookieValue;
    // }
});
