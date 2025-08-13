// // static/js/register.js

// $(document).ready(function () {
//     console.log("✅ Registration script loaded");

//     $("#signup_btn").click(function (e) {
//         e.preventDefault();

//         $("#acknowledge").text("");
//         const isValid = validateRegistrationForm();

//         if (!isValid) return;

//         const firstName = $("#first_name").val().trim();
//         const lastName = $("#last_name").val().trim();
//         const username = $("#username").val().trim();
//         const email = $("#email").val().trim();
//         const password = $("#password").val();
//         const confirmPassword = $("#confirm_password").val();
//         const gender = $("input[name='gender']:checked").val();
//         const dob = $("#dob").val();
//         const role = $("#role").val();
//         const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

//         // Email uniqueness check before submission
//         validateEmailUniqueness(email, function (isAvailable) {
//             if (!isAvailable) return;

//             $.ajax({
//                 url: "/account/registration/",
//                 method: "POST",
//                 data: {
//                     first_name: firstName,
//                     last_name: lastName,
//                     username: username,
//                     email: email,
//                     password: password,
//                     confirm_password: confirmPassword,
//                     gender: gender,
//                     dob: dob,
//                     role: role,
//                     csrfmiddlewaretoken: csrfToken
//                 },
//                 beforeSend: function () {
//                     $("#spinner-overlay").show();
//                 },
//                 success: function (response) {
//                     $("#acknowledge").text(response.message)
//                         .css("color", "green").fadeIn().delay(5000).fadeOut();
//                     setTimeout(() => {
//                         window.location.href = response.redirect_url;
//                     }, 7000);
//                 },
//                 error: function (xhr) {
//                     const res = xhr.responseJSON;
//                     if (res.errors) {
//                         for (const field in res.errors) {
//                             $(`#${field}_error`).html(`<div class="text-danger">${res.errors[field]}</div>`);
//                         }
//                     } else {
//                         $("#acknowledge").html(`<div class="alert alert-danger">Something went wrong!</div>`);
//                     }
//                 },
//                 complete: function () {
//                     $("#spinner-overlay").hide();
//                 }
//             });
//         });
//     });
    
function validateRegistrationForm() {
    const firstName = $("#first_name").val()
    const lastName = $("#last_name").val()
    const username = $("#username").val()
    const email = $("#email").val()
    const password = $("#password").val();
    const confirmPassword = $("#confirm_password").val();
    const dob = $("#dob").val();
    const gender = $("input[name='gender']:checked").val();

    let isValid = true;

    // Clear previous errors
    $(".text-danger").html('');

    const nameRegex = /^[A-Za-z]{2,30}$/;
    const usernameRegex = /^[A-Za-z0-9_]{4,20}$/;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/;

    const today = new Date();

    if (!firstName) {
        $("#first_name_error").html("First name is required.");
        isValid = false;
    } else if (!nameRegex.test(firstName)) {
        $("#first_name_error").html("Only letters allowed (2–30 characters).");
        isValid = false;
    }

    if (!lastName) {
        $("#last_name_error").html("Last name is required.");
        isValid = false;
    } else if (!nameRegex.test(lastName)) {
        $("#last_name_error").html("Only letters allowed (2–30 characters).");
        isValid = false;
    }

    if (!username) {
        $("#username_error").html("Username is required.");
        isValid = false;
    } else if (!usernameRegex.test(username)) {
        $("#username_error").html("Use 4–20 characters: letters, numbers, underscores.");
        isValid = false;
    }

    if (!email) {
        $("#email_error").html("Email is required.");
        isValid = false;
    } else if (!emailRegex.test(email)) {
        $("#email_error").html("Invalid email format.");
        isValid = false;
    }

    if (!password) {
        $("#password_error").html("Password is required.");
        isValid = false;
    } else if (!passwordRegex.test(password)) {
        $("#password_error").html("Password must include uppercase, lowercase, number, and special char.");
        isValid = false;
    }

    if (!confirmPassword) {
        $("#confirm_password_error").html("Please confirm your password.");
        isValid = false;
    } else if (password !== confirmPassword) {
        $("#confirm_password_error").html("Passwords do not match.");
        isValid = false;
    }

    if (!gender) {
        $("#gender_error").html("Please select a gender.");
        isValid = false;
    }

    if (!dob) {
        $("#dob_error").html("Date of birth is required.");
        isValid = false;
    } else {
        const dobDate = new Date(dob);
        if (dobDate > today) {
            $("#dob_error").html("DOB cannot be in the future.");
            isValid = false;
        } else {
            const age = today.getFullYear() - dobDate.getFullYear();
            const m = today.getMonth() - dobDate.getMonth();
            const actualAge = m > 0 || (m === 0 && today.getDate() >= dobDate.getDate()) ? age : age - 1;
            if (actualAge < 10) {
                $("#dob_error").html("You must be at least 10 years old.");
                isValid = false;
            }
        }
    }

    $("#signup_btn").prop("disabled", !isValid);
    return isValid;
}
function validateEmailUniqueness(email, callback) {
    $.ajax({
        url: "/account/check_email/",
        type: "POST",
        data: {
            email: email,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function (res) {
            if (res.exists) {
                $("#email_error").html("Email already taken.");
                callback(false);
            } else {
                callback(true);
            }
        },
        error: function () {
            $("#email_error").html("Could not check email.");
            callback(false);
        }
    });
}


$(document).ready(function () {
    console.log("✅ Registration script loaded");

    $("input, select").on("input change blur", function () {
        validateRegistrationForm();
    });

    $("#signup_btn").click(function (e) {
        e.preventDefault();
        $("#acknowledge").text("");

        if (!validateRegistrationForm()) return;

        const formData = {
            first_name: $("#first_name").val().trim(),
            last_name: $("#last_name").val().trim(),
            username: $("#username").val().trim(),
            email: $("#email").val().trim(),
            password: $("#password").val(),
            confirm_password: $("#confirm_password").val(),
            gender: $("input[name='gender']:checked").val(),
            dob: $("#dob").val(),
            role: $("#role").val(),
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        };

        validateEmailUniqueness(formData.email, function (isAvailable) {
            if (!isAvailable) return;

            $.ajax({
                url: "/account/registration/",
                method: "POST",
                data: formData,
                beforeSend: function () {
                    $("#spinner-overlay").show();
                },
                success: function (response) {
                    $("#acknowledge").text(response.message).css("color", "green").fadeIn().delay(5000).fadeOut();
                    setTimeout(() => {
                        window.location.href = response.redirect_url;
                    }, 7000);
                },
                error: function (xhr) {
                    const res = xhr.responseJSON;
                    if (res.errors) {
                        for (const field in res.errors) {
                            $(`#${field}_error`).html(`<div class="text-danger">${res.errors[field]}</div>`);
                        }
                    } else {
                        $("#acknowledge").html(`<div class="alert alert-danger">Something went wrong!</div>`);
                    }
                },
                complete: function () {
                    $("#spinner-overlay").hide();
                }
            });
        });
    });

    


    // ✅ Handle login with AJAX
    $("#login-btn").click(function (e) {
        e.preventDefault();

        const email = $("#email").val().trim();
        const password = $("#password").val().trim();
        const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        if (!email || !password) {
            alert("Please enter both email and password.");
            return;
        }

        $("#login-btn").prop("disabled", true);

        $.ajax({
            url: "/account/login_view/",
            method: "POST",
            data: {
                email: email,
                password: password,
                csrfmiddlewaretoken: csrfToken
            },
            headers: {
                "X-CSRFToken": csrfToken
            },
            success: function (response) {
                if (response.status === "success") {
                    window.location.href = response.redirect_url;
                } else {
                    alert("Login failed: " + response.message);
                    $("#login-btn").prop("disabled", false);
                }
            },
            error: function () {
                alert("Login failed due to server error.");
                $("#login-btn").prop("disabled", false);
            }
        });
    });

});    




