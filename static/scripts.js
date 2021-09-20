/*** Functions ***/
const checkFormRegistration = (event) => {
    const username = document.querySelector("#register_username").value.trim();
    const password = document.querySelector("#register_password").value.trim();
    const password_confirmation = document.querySelector("#register_password_confirmation").value.trim();
    const register_message = document.querySelector("#register_message");
    const fullname = document.querySelector("#register_fullname").value.trim();
    const age = document.querySelector("#register_age").value.trim();
    const experience = document.querySelector("#register_experience").value.trim();
    const specialty = document.querySelector("#register_specialty").value.trim();

    register_message.innerHTML = "";

    if (username.length === 0) {
        register_message.innerHTML += "<li><p class='red'>Please provide a username</p></li>";
        document.querySelector("#modal_warning").click();
        event.preventDefault();
    }
    if (password.length === 0) {
         register_message.innerHTML += "<li><p class='red'>Please provide a password</p></li>";
         document.querySelector("#modal_warning").click();
         event.preventDefault();
    }
    if (password_confirmation.length === 0) {
        register_message.innerHTML += "<li><p class='red'>Please provide a password confirmation</p></li>";
        document.querySelector("#modal_warning").click();
        event.preventDefault();
    }
    if (password.length > 0 && password_confirmation.length > 0 && password !== password_confirmation) {
        register_message.innerHTML += "<li><p class='red'>Passwords do not match</p></li>";
        document.querySelector("#modal_warning").click();
        event.preventDefault();
    }
    if (password.length > 0 && password.length < 6) {
        register_message.innerHTML += "<li><p class='red'>Password must be at least 6 characters long.</p></li>";
        document.querySelector("#modal_warning").click();
        event.preventDefault();
    }

    if (fullname.length === 0) {
        register_message.innerHTML += "<li><p class='red'>Please provide your full name</p></li>";
        document.querySelector("#modal_warning").click();
        event.preventDefault();
    }

    if (age.length === 0) {
        register_message.innerHTML += "<li><p class='red'>Please provide your age</p></li>";
        document.querySelector("#modal_warning").click();
        event.preventDefault();
    }

    if (age < 0) {
        register_message.innerHTML += "<li><p class='red'>Age must be a positive integer</p></li>";
        document.querySelector("#modal_warning").click();
        event.preventDefault();
    }

    if (experience.length === 0) {
        register_message.innerHTML += "<li><p class='red'>Please provide your experience</p></li>";
        document.querySelector("#modal_warning").click();
        event.preventDefault();
    }

    if (experience < 0) {
        register_message.innerHTML += "<li><p class='red'>Experience must be a positive integer</p></li>";
        document.querySelector("#modal_warning").click();
        event.preventDefault();
    }

    if (specialty.length === 0) {
        register_message.innerHTML += "<li><p class='red'>Please provide your specialty</p></li>";
        document.querySelector("#modal_warning").click();
        event.preventDefault();
    }
}

const checkFormLogin = (event) => {
    const username = document.querySelector("#login_username").value.trim();
    const password = document.querySelector("#login_password").value.trim();
    const login_message = document.querySelector("#login_message");

    login_message.innerHTML = "";

    if (username.length === 0) {
        login_message.innerHTML += "<li><p class='red'>Please provide a username</p></li>";
        event.preventDefault();
    }
    if (password.length === 0) {
         login_message.innerHTML += "<li><p class='red'>Please provide a password</p></li>";
         event.preventDefault();
    }
}

const checkFormNewPatient = (event) => {
    const patient_fullname = document.querySelector("#patient_fullname").value.trim();
    const patient_age = document.querySelector("#patient_age").value.trim();
    const patient_address = document.querySelector("#patient_address").value.trim();
    const patient_religion = document.querySelector("#patient_religion").value.trim();
    const patient_occupation = document.querySelector("#patient_occupation").value.trim();
    const patient_race = document.querySelector("#patient_race").value.trim();
    const patient_nationality = document.querySelector("#patient_nationality").value.trim();
    const passport_number = document.querySelector("#passport_number").value.trim();
    const social_history_message = document.querySelector("#social_history_message");
    const regex_number = /^\d+$/;

    social_history_message.innerHTML = "";

    if (patient_fullname.length === 0) {
        social_history_message.innerHTML+= "<li><p class='red'>Please provide patient's full name</p></li>";
        document.querySelector("#modal_warning_new_patient").click();
        event.preventDefault();
    }
    if (patient_age.length === 0) {
        social_history_message.innerHTML+= "<li><p class='red'>Please provide patient's age</p></li>";
        document.querySelector("#modal_warning_new_patient").click();
        event.preventDefault();
    }
    if (passport_number.length === 0) {
        social_history_message.innerHTML+= "<li><p class='red'>Please provide passport number</p></li>";
        document.querySelector("#modal_warning_new_patient").click();
        event.preventDefault();
    }
    if (patient_address.length === 0) {
        social_history_message.innerHTML+= "<li><p class='red'>Please provide patient's address</p></li>";
        document.querySelector("#modal_warning_new_patient").click();
        event.preventDefault();
    }
    if (patient_religion.length === 0) {
        social_history_message.innerHTML+= "<li><p class='red'>Please provide patient's religion</p></li>";
        document.querySelector("#modal_warning_new_patient").click();
        event.preventDefault();
    }
    if (patient_race.length === 0) {
        social_history_message.innerHTML+= "<li><p class='red'>Please provide patient's race</p></li>";
        document.querySelector("#modal_warning_new_patient").click();
        event.preventDefault();
    }
    if (patient_nationality.length === 0) {
        social_history_message.innerHTML+= "<li><p class='red'>Please provide patient's nationality</p></li>";
        document.querySelector("#modal_warning_new_patient").click();
        event.preventDefault();
    }

    if (patient_age.length > 0 && patient_age <= 0) {
        social_history_message.innerHTML+= "<li><p class='red'>Age must be a positive integer</p></li>";
        document.querySelector("#modal_warning_new_patient").click();
        event.preventDefault();
    }

    if (passport_number.length > 0 && passport_number <= 0) {
        social_history_message.innerHTML+= "<li><p class='red'>Passport number must be a positive integer</p></li>";
        document.querySelector("#modal_warning_new_patient").click();
        event.preventDefault();
    }

    if (!regex_number.test(patient_age)) {
        social_history_message.innerHTML+= "<li><p class='red'>Age must be a positive integer</p></li>";
        document.querySelector("#modal_warning_new_patient").click();
        event.preventDefault();
    }

    if (!regex_number.test(passport_number)) {
        social_history_message.innerHTML+= "<li><p class='red'>Passport number must be a positive integer</p></li>";
        document.querySelector("#modal_warning_new_patient").click();
        event.preventDefault();
    }
}

const checkFormDiseases = (event) => {
    const disease_name = document.querySelector("#disease_name").value.trim();
    const disease_description = document.querySelector("#disease_description").value.trim();
    const disease_date_of_diagnonis = document.querySelector("#disease_date_of_diagnosis").value.trim();
    const disease_end_of_treatment = document.querySelector("#disease_end_of_treatment").value.trim();
    const disease_medication_dosage = document.querySelector("#disease_medication_dosage").value.trim();
    const diseases_message = document.querySelector("#diseases_message");
    const date_format_regex = /^\d{4}-\d{2}-\d{2}$/;
    const whole_numbers_regex = /^\d+$/;

    diseases_message.innerHTML = "";

    if (disease_name.length === 0) {
        diseases_message.innerHTML+= "<li><p class='red'>Please provide name of the disease </p></li>";
        document.querySelector("#modal_warning_diseases").click();
        event.preventDefault();
    }

    if (disease_description.length === 0) {
        diseases_message.innerHTML+= "<li><p class='red'>Please provide disease's description </p></li>";
        document.querySelector("#modal_warning_diseases").click();
        event.preventDefault();
    }

    if (disease_date_of_diagnosis.value.length === 0) {
        diseases_message.innerHTML+= "<li><p class='red'>Please provide the date when the disease was diagnosed </p></li>";
        document.querySelector("#modal_warning_diseases").click();
        event.preventDefault();
    }

    if (disease_date_of_diagnosis.value.length > 0 && !date_format_regex.test(disease_date_of_diagnosis.value)) {
        diseases_message.innerHTML+= "<li><p class='red'>Please provide the date of diagnosis in the correct format: yyyy-mm-dd (example: 2021-09-02) </p></li>";
        document.querySelector("#modal_warning_diseases").click();
        event.preventDefault();
    }

    if (disease_end_of_treatment.length > 0 && !date_format_regex.test(disease_end_of_treatment)) {
        diseases_message.innerHTML+= "<li><p class='red'>Please provide the final date of treatment in the correct format: yyyy-mm-dd (example: 2021-09-02) </p></li>";
        document.querySelector("#modal_warning_diseases").click();
        event.preventDefault();
    }
}


const checkFormAllergies = (event) => {
    const allergy_name = document.querySelector("#allergy_name").value.trim();
    const allergy_description = document.querySelector("#allergy_description").value.trim();
    const allergy_date_of_diagnonis = document.querySelector("#allergy_date_of_diagnosis").value.trim();
    const allergy_end_of_treatment = document.querySelector("#allergy_end_of_treatment").value.trim();
    const allergy_medication_dosage = document.querySelector("#allergy_medication_dosage").value.trim();
    const allergies_message = document.querySelector("#allergies_message");
    const date_format_regex = /^\d{4}-\d{2}-\d{2}$/;
    const whole_numbers_regex = /^\d+$/;

    allergies_message.innerHTML = "";

    if (allergy_name.length === 0) {
        allergies_message.innerHTML+= "<li><p class='red'>Please provide name of the allergy </p></li>";
        document.querySelector("#modal_warning_allergies").click();
        event.preventDefault();
    }

    if (allergy_description.length === 0) {
        allergies_message.innerHTML+= "<li><p class='red'>Please provide allergy's description </p></li>";
        document.querySelector("#modal_warning_allergies").click();
        event.preventDefault();
    }

    if (allergy_date_of_diagnosis.value.length === 0) {
        allergies_message.innerHTML+= "<li><p class='red'>Please provide the date when the allergy was diagnosed </p></li>";
        document.querySelector("#modal_warning_allergies").click();
        event.preventDefault();
    }

    if (allergy_date_of_diagnosis.value.length > 0 && !date_format_regex.test(allergy_date_of_diagnosis.value)) {
        allergies_message.innerHTML+= "<li><p class='red'>Please provide the date of diagnosis in the correct format: yyyy-mm-dd (example: 2021-09-02) </p></li>";
        document.querySelector("#modal_warning_allergies").click();
        event.preventDefault();
    }

    if (allergy_end_of_treatment.length > 0 && !date_format_regex.test(allergy_end_of_treatment)) {
        allergies_message.innerHTML+= "<li><p class='red'>Please provide the final date of treatment in the correct format: yyyy-mm-dd (example: 2021-09-02) </p></li>";
        document.querySelector("#modal_warning_allergies").click();
        event.preventDefault();
    }
}


const checkFormSurgicalHistory = (event) => {
    const surgery_name = document.querySelector("#surgery_name").value.trim();
    const surgery_description = document.querySelector("#surgery_description").value.trim();
    const surgery_date = document.querySelector("#surgery_date").value.trim();
    const surgery_preopertive_diagnosis = document.querySelector("#surgery_preopertive_diagnosis").value.trim();
    const surgery_postoperative_diagnosis = document.querySelector("#surgery_postoperative_diagnosis").value.trim();
    const condition_after_surgery = document.querySelector("#condition_after_surgery").value.trim();
    const surgical_history_message = document.querySelector("#surgical_history_message");
    const date_format_regex = /^\d{4}-\d{2}-\d{2}$/;
    const whole_numbers_regex = /^\d+$/;

    surgical_history_message.innerHTML = "";

    if (surgery_name.length === 0) {
        surgical_history_message.innerHTML+= "<li><p class='red'>Please provide surgery name </p></li>";
        document.querySelector("#modal_warning_surgical_history").click();
        event.preventDefault();
    }

    if (surgery_description.length === 0) {
        surgical_history_message.innerHTML+= "<li><p class='red'>Please provide surgery description </p></li>";
        document.querySelector("#modal_warning_surgical_history").click();
        event.preventDefault();
    }

    if (surgery_date.length === 0) {
        surgical_history_message.innerHTML+= "<li><p class='red'>Please provide surgery date </p></li>";
        document.querySelector("#modal_warning_surgical_history").click();
        event.preventDefault();
    }

    if (surgery_preopertive_diagnosis.length === 0) {
        surgical_history_message.innerHTML+= "<li><p class='red'>Please provide surgery preopertive diagnosis </p></li>";
        document.querySelector("#modal_warning_surgical_history").click();
        event.preventDefault();
    }

    if (surgery_postoperative_diagnosis.length === 0) {
        surgical_history_message.innerHTML+= "<li><p class='red'>Please provide surgery postoperative diagnosis </p></li>";
        document.querySelector("#modal_warning_surgical_history").click();
        event.preventDefault();
    }

    if (condition_after_surgery.length === 0) {
        surgical_history_message.innerHTML+= "<li><p class='red'>Please provide description of the patient's condition after the surgery </p></li>";
        document.querySelector("#modal_warning_surgical_history").click();
        event.preventDefault();
    }

    if (surgery_date.length > 0 && !date_format_regex.test(surgery_date)) {
        surgical_history_message.innerHTML += "<li><p class='red'>Please provide the date of surgery in the correct format: yyyy-mm-dd (example: 2021-09-02) </p></li>";
        document.querySelector("#modal_warning_surgical_history").click();
        event.preventDefault();
    }
}


const checkFormFamilyHistory = (event) => {
    const relative_name = document.querySelector("#relative_name").value.trim();
    const relative_status = document.querySelector("#relative_status").value.trim();
    const relative_gender = document.querySelector("#relative_gender").value.trim();
    const relative_age = document.querySelector("#relative_age").value.trim();
    const family_history_message = document.querySelector("#family_history_message");
    const whole_numbers_regex = /^\d+$/;

    family_history_message.innerHTML = "";

    if (relative_name.length === 0) {
        family_history_message.innerHTML+= "<li><p class='red'>Please provide relative name </p></li>";
        document.querySelector("#modal_warning_family_history").click();
        event.preventDefault();
    }

    if (relative_status.length === 0) {
        family_history_message.innerHTML+= "<li><p class='red'>Please provide relative status </p></li>";
        document.querySelector("#modal_warning_family_history").click();
        event.preventDefault();
    }

    if (relative_age.length === 0) {
        family_history_message.innerHTML+= "<li><p class='red'>Please provide relative age </p></li>";
        document.querySelector("#modal_warning_family_history").click();
        event.preventDefault();
    }

    // numbers
    const relative_age_regex_test = whole_numbers_regex.test(relative_age);

    if (relative_age.length > 0 && !relative_age_regex_test) {
        family_history_message.innerHTML+= "<li><p class='red'> relative age must be a positive integer </p></li>";
        document.querySelector("#modal_warning_family_history").click();
        event.preventDefault();
    }
}


const checkFormHabits = (event) => {
    const habit_name = document.querySelector("#habit_name").value.trim();
    const habit_year = document.querySelector("#habit_year").value.trim();
    const habits_message = document.querySelector("#habits_message");
    const whole_numbers_regex = /^\d+$/;

    habits_message.innerHTML = "";

    if (habit_name.length === 0) {
        habits_message.innerHTML+= "<li><p class='red'>Please provide habit name </p></li>";
        document.querySelector("#modal_warning_habits").click();
        event.preventDefault();
    }

    if (habit_year.length === 0) {
        habits_message.innerHTML+= "<li><p class='red'>Please provide the year when the habit started </p></li>";
        document.querySelector("#modal_warning_habits").click();
        event.preventDefault();
    }

    // numbers
    const habit_year_regex_test = whole_numbers_regex.test(habit_year);

    if (habit_year.length > 0 && !habit_year_regex_test) {
        habits_message.innerHTML+= "<li><p class='red'> Year must be a positive integer </p></li>";
        document.querySelector("#modal_warning_habits").click();
        event.preventDefault();
    }
}


const checkFormImmunizationHistory = (event) => {
    const immunization_name = document.querySelector("#immunization_name").value.trim();
    const immunization_date = document.querySelector("#immunization_date").value.trim();
    const immunization_history_message = document.querySelector("#immunization_history_message");
    const date_format_regex = /^\d{4}-\d{2}-\d{2}$/;
    const whole_numbers_regex = /^\d+$/;

    immunization_history_message.innerHTML = "";

    if (immunization_name.length === 0) {
        immunization_history_message.innerHTML+= "<li><p class='red'>Please provide immunization name </p></li>";
        document.querySelector("#modal_warning_immunization_history").click();
        event.preventDefault();
    }

    if (immunization_date.length === 0) {
        immunization_history_message.innerHTML+= "<li><p class='red'>Please provide immunization date </p></li>";
        document.querySelector("#modal_warning_immunization_history").click();
        event.preventDefault();
    }

    if (immunization_date.length > 0 && !date_format_regex.test(immunization_date)) {
        immunization_history_message.innerHTML+= "<li><p class='red'> Please provide the date in the correct format: yyyy-mm-dd (example: 2021-09-02) </p></li>";
        document.querySelector("#modal_warning_immunization_history").click();
        event.preventDefault();
    }
}


const checkFormTestsResults = (events) => {
    const test_name = document.querySelector("#test_name").value.trim();
    const test_date = document.querySelector("#test_date").value.trim();
    const test_result_description = document.querySelector("#test_result_description").value.trim();
    const tests_results_message = document.querySelector("#tests_results_message");
    const date_format_regex = /^\d{4}-\d{2}-\d{2}$/;

    tests_results_message.innerHTML = "";

    if (test_name.length === 0) {
        tests_results_message.innerHTML+= "<li><p class='red'>Please provide test name </p></li>";
        document.querySelector("#modal_warning_tests_results").click();
        event.preventDefault();
    }

    if (test_date.length === 0) {
        tests_results_message.innerHTML+= "<li><p class='red'>Please provide test date</p></li>";
        document.querySelector("#modal_warning_tests_results").click();
        event.preventDefault();
    }

    if (test_result_description.length === 0) {
        tests_results_message.innerHTML+= "<li><p class='red'>Please provide test result description</p></li>";
        document.querySelector("#modal_warning_tests_results").click();
        event.preventDefault();
    }

    if (test_date.length > 0 && !date_format_regex.test(test_date)) {
        tests_results_message.innerHTML+= "<li><p class='red'> Please provide date in the correct format: yyyy-mm-dd (example: 2021-09-02) </p></li>";
        document.querySelector("#modal_warning_tests_results").click();
        event.preventDefault();
    }
}


/*** Event listeners ***/
if (document.querySelector("#register_button") != undefined) {
   document.querySelector("#register_button").addEventListener("click", checkFormRegistration);
}

if (document.querySelector("#login_button") != undefined) {
   document.querySelector("#login_button").addEventListener("click", checkFormLogin);
}

if (document.querySelector("#patient_register_button") != undefined) {
    document.querySelector("#patient_register_button").addEventListener("click", checkFormNewPatient);
}

if (document.querySelector("#disease_button") != undefined) {
    document.querySelector("#disease_button").addEventListener("click", checkFormDiseases);
}

if (document.querySelector("#allergy_button") != undefined) {
    document.querySelector("#allergy_button").addEventListener("click", checkFormAllergies);
}

if (document.querySelector("#surgical_history_button") != undefined) {
    document.querySelector("#surgical_history_button").addEventListener("click", checkFormSurgicalHistory);
}

if (document.querySelector("#family_history_button") != undefined) {
    document.querySelector("#family_history_button").addEventListener("click", checkFormFamilyHistory);
}

if (document.querySelector("#habits_button") != undefined) {
    document.querySelector("#habits_button").addEventListener("click", checkFormHabits);
}

if (document.querySelector("#immunization_history_button") != undefined) {
    document.querySelector("#immunization_history_button").addEventListener("click", checkFormImmunizationHistory);
}

if (document.querySelector("#tests_results_button") != undefined) {
    document.querySelector("#tests_results_button").addEventListener("click", checkFormTestsResults);
}
