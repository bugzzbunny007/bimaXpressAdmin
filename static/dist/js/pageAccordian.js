console.log('javascript is working');

window.onload = function () {

    var ex1 = document.getElementById('nanana');
    ex1.onclick = handler;
    var ex2 = document.getElementById('nanana2');
    ex2.onclick = yeshandler;


    var physicianYes = document.getElementById('physicianYes');
    physicianYes.onclick = physicianYesclick;
    var physicianNo = document.getElementById('physicianNo');
    physicianNo.onclick = physicianNoclick;


    var investigation = document.getElementById('investigation');
    investigation.onclick = investigationClickMadical_managmentClick;
    var madical_managment = document.getElementById('madical_managment');
    madical_managment.onclick = investigationClickMadical_managmentClick;
    var surgical = document.getElementById('surgical');
    surgical.onclick = surgicalClick;

    var policeReportYes = document.getElementById('policeReportYes').onclick = function () {
        document.getElementById('forFirNum').innerHTML = `
      <label for="exampleInputEmail1">FIR No.</label>
                        <input class="form-control" name="doctor_firNo" type="tel"
                          value="">
      `;
    }
    var policeReportNo = document.getElementById('policeReportNo').onclick = function () {
        document.getElementById('forFirNum').innerHTML = ``;
    }
}

function handler() {
    var onclickYes = document.getElementById('onclickYes');
    onclickYes.innerHTML = `
  <label for="exampleInputEmail1">Company Name</label>
                          <input class="form-control" name="patient_details_HealthInsuranceYesCompanyName" type="text"
                            value="">

                            <label for="exampleInputEmail1">Give Details</label>
                          <input class="form-control" name="Give_details" type="text"
                            value="">
  `;
}
function yeshandler() {
    var onclickYes = document.getElementById('onclickYes');
    onclickYes.innerHTML = ``;
}


function physicianYesclick() {
    var onclickYesPhysician = document.getElementById('onclickYesPhysician');
    onclickYesPhysician.innerHTML = `
    <label for="exampleInputEmail1">Physician Name</label>
                      <input class="form-control" name="patient_details_familyPhysicianYesPhysicianName" type="text"
                        value="">

                        <label for="exampleInputEmail1">Physician Contact Number</label>
                      <input class="form-control" name="patient_details_familyPhysicianYesPhysicianContactNum" type="tel"
                        value="">
  `;
}
function physicianNoclick() {
    var onclickYesPhysician = document.getElementById('onclickYesPhysician');
    onclickYesPhysician.innerHTML = ``;
}

function investigationClickMadical_managmentClick() {
    alert('redirecting to administration')
    var forLineOfTreatment = document.getElementById('forLineOfTreatment');
    forLineOfTreatment.innerHTML = ``;

}
function surgicalClick() {
    var forLineOfTreatment = document.getElementById('forLineOfTreatment');
    forLineOfTreatment.innerHTML = `
    <label for="exampleInputEmail1">ICD 10 PCS code </label>
                      <input class="form-control" name="doctor_icd_10PcsCode" type="tel"
                        value="">
    `;
}
function testAlcohol() {
    document.getElementById('testAlcohol').innerHTML=`
    
    <label for="exampleInputEmail1">Upload Documents</label> <br>
    <input type="file" name="doctor_testAlcoholUploadDocument" >
    `;
}

var sidenav = document.getElementById("sidenav");

function navHover() {
  sidenav.innerHTML = `<div><i class="glyphicon glyphicon-home activeIcon"></i><b>Home</b></div>
    <div><i class="glyphicon glyphicon-plus"></i><b>New-Claim</b></div>
    <div><i class="glyphicon glyphicon-envelope"></i><b>Inbox</b></div>
    <div><i class="glyphicon glyphicon-user"></i><b>Profile</b></div>
    <div><i class="glyphicon glyphicon-cog"></i><b>Settings</b></div>`;
}
function mainHover() {
  sidenav.innerHTML = `<div><i class="glyphicon glyphicon-home activeIcon"></i></div>
    <div><i class="glyphicon glyphicon-plus"></i></div>
    <div><i class="glyphicon glyphicon-envelope"></i></div>
    <div><i class="glyphicon glyphicon-user"></i></div>
    <div><i class="glyphicon glyphicon-cog"></i></div>`;
}