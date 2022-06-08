function editProfile() {
    var x = document.getElementById("form_profile");
    var fullname = document.getElementById("full_name")

    if (x.style.display === "none") {
        x.style.display = "block";
        fullname.readOnly = false;

    } else {
        x.style.display = "none";
        fullname.readOnly = true;
    }
}