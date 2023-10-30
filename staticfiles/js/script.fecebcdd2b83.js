document.addEventListener("DOMContentLoaded", function () {
  var elems = document.querySelectorAll(".sidenav");
  var instances = M.Sidenav.init(elems);
});

document.addEventListener("DOMContentLoaded", function () {
  const dateEl = document.getElementById("id_date");
  if (dateEl) {
    M.Datepicker.init(dateEl, {
      format: "yyyy-mm-dd",
      defaultDate: new Date(),
      setDefaultDate: true,
      autoClose: true,
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    const timeEl = document.getElementById("id_time");
    M.Timepicker.init(timeEl, {
      showClearBtn: true, // Add a clear button
      twelveHour: false, // Use 24-hour format, false for 24 hour
    });
  });

  const dateIssuedEl = document.getElementById("id_date_issued");
  if (dateIssuedEl) {
    M.Datepicker.init(dateIssuedEl, {
      format: "yyyy-mm-dd",
      defaultDate: new Date(),
      setDefaultDate: true,
      autoClose: true,
    });
  }

  const selectEl = document.getElementById("id_care_provider");
  M.FormSelect.init(selectEl);
});
