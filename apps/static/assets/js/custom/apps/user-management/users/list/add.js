"use strict";

var KTUsersAddUser = (function () {
  const modalElement = document.getElementById("kt_modal_add_user");
  const formElement = modalElement.querySelector("#kt_modal_add_user_form");
  const modalInstance = new bootstrap.Modal(modalElement);

  return {
    init: function () {
      (function () {
        const formValidation = FormValidation.formValidation(formElement, {
          fields: {
            user_name: {
              validators: {
                notEmpty: {
                  message: "Full name is required",
                },
              },
            },
            user_email: {
              validators: {
                notEmpty: {
                  message: "Valid email address is required",
                },
              },
            },
          },
          plugins: {
            trigger: new FormValidation.plugins.Trigger(),
            bootstrap: new FormValidation.plugins.Bootstrap5({
              rowSelector: ".fv-row",
              eleInvalidClass: "",
              eleValidClass: "",
            }),
          },
        });

        const submitButton = modalElement.querySelector(
          '[data-kt-users-modal-action="submit"]'
        );

        submitButton.addEventListener("click", (event) => {
          event.preventDefault();
          if (formValidation) {
            formValidation.validate().then((status) => {
              console.log("validated!");
              if (status === "Valid") {
                submitButton.setAttribute("data-kt-indicator", "on");
                submitButton.disabled = true;

                setTimeout(() => {
                  submitButton.removeAttribute("data-kt-indicator");
                  submitButton.disabled = false;

                  Swal.fire({
                    text: "Form has been successfully submitted!",
                    icon: "success",
                    buttonsStyling: false,
                    confirmButtonText: "Ok, got it!",
                    customClass: {
                      confirmButton: "btn btn-primary",
                    },
                  }).then((result) => {
                    if (result.isConfirmed) {
                      modalInstance.hide();
                    }
                  });
                }, 2000);
              } else {
                Swal.fire({
                  text:
                    "Sorry, looks like there are some errors detected, please try again.",
                  icon: "error",
                  buttonsStyling: false,
                  confirmButtonText: "Ok, got it!",
                  customClass: {
                    confirmButton: "btn btn-primary",
                  },
                });
              }
            });
          }
        });

        const cancelButton = modalElement.querySelector(
          '[data-kt-users-modal-action="cancel"]'
        );

        cancelButton.addEventListener("click", (event) => {
          event.preventDefault();
          Swal.fire({
            text: "Are you sure you would like to cancel?",
            icon: "warning",
            showCancelButton: true,
            buttonsStyling: false,
            confirmButtonText: "Yes, cancel it!",
            cancelButtonText: "No, return",
            customClass: {
              confirmButton: "btn btn-primary",
              cancelButton: "btn btn-active-light",
            },
          }).then((result) => {
            if (result.value) {
              formElement.reset();
              modalInstance.hide();
            } else if (result.dismiss === "cancel") {
              Swal.fire({
                text: "Your form has not been cancelled!",
                icon: "error",
                buttonsStyling: false,
                confirmButtonText: "Ok, got it!",
                customClass: {
                  confirmButton: "btn btn-primary",
                },
              });
            }
          });
        });

        const closeButton = modalElement.querySelector(
          '[data-kt-users-modal-action="close"]'
        );

        closeButton.addEventListener("click", (event) => {
          event.preventDefault();
          Swal.fire({
            text: "Are you sure you would like to cancel?",
            icon: "warning",
            showCancelButton: true,
            buttonsStyling: false,
            confirmButtonText: "Yes, cancel it!",
            cancelButtonText: "No, return",
            customClass: {
              confirmButton: "btn btn-primary",
              cancelButton: "btn btn-active-light",
            },
          }).then((result) => {
            if (result.value) {
              formElement.reset();
              modalInstance.hide();
            } else if (result.dismiss === "cancel") {
              Swal.fire({
                text: "Your form has not been cancelled!",
                icon: "error",
                buttonsStyling: false,
                confirmButtonText: "Ok, got it!",
                customClass: {
                  confirmButton: "btn btn-primary",
                },
              });
            }
          });
        });
      })();
    },
  };
})();

KTUtil.onDOMContentLoaded(() => {
  KTUsersAddUser.init();
});
