let business_segment_list = []
let type_list = []
let insured_state_list = []
let broker_company_list = []
let broker_state_list = []
let underwriter_team_list = []
let business_classification_list = []

let forms_res = []
$( document ).ready(function() {
    console.log( "ready!" );

    $.ajax({
        url: "http://localhost:5000/getbusinesssegmet",
        type: 'GET',
        dataType: 'json', // added data type,
        success: function(res) {
            console.log(res);
            business_segment_list = res.list_of_data
        },

    }).done(function(){
		insertSelectOptions('BusinessSegment', business_segment_list)
    });

    $.ajax({
        url: "http://localhost:5000/gettype",
        type: 'GET',
        dataType: 'json', // added data type,
        success: function(res) {
            console.log(res);
            type_list = res.list_of_data
        },

    }).done(function(){
		insertSelectOptions('Type', type_list)
    });

	$.ajax({
        url: "http://localhost:5000/getinsuredstate",
        type: 'GET',
        dataType: 'json', // added data type,
        success: function(res) {
            console.log(res);
            insured_state_list = res.list_of_data
        },

    }).done(function(){
		insertSelectOptions('InsuredState', insured_state_list)
    });

    $.ajax({
        url: "http://localhost:5000/getbrokercompany",
        type: 'GET',
        dataType: 'json', // added data type,
        success: function(res) {
            console.log(res);
            broker_company_list = res.list_of_data
        },

    }).done(function(){
		insertSelectOptions('BrokerCompany', broker_company_list)
    });

    $.ajax({
        url: "http://localhost:5000/getbrokerstate",
        type: 'GET',
        dataType: 'json', // added data type,
        success: function(res) {
            console.log(res);
            broker_state_list = res.list_of_data
        },

    }).done(function(){
		insertSelectOptions('BrokerState', broker_state_list)
    });

    $.ajax({
        url: "http://localhost:5000/getunderwriterteam",
        type: 'GET',
        dataType: 'json', // added data type,
        success: function(res) {
            console.log(res);
            underwriter_team_list = res.list_of_data
        },

    }).done(function(){
		insertSelectOptions('UnderwriterTeam', underwriter_team_list)
    });

    $.ajax({
        url: "http://localhost:5000/getbusinessclassification",
        type: 'GET',
        dataType: 'json', // added data type,
        success: function(res) {
            console.log(res);
            business_classification_list = res.list_of_data
        },

    }).done(function(){
		insertSelectOptions('BusinessClassification', business_classification_list)
    });

    const url = ''

	createCheckboxes()

	selectFormFieldIds = Array.from(document.getElementById('formId')
                             .getElementsByTagName('select'))
                             .map(el => el.id)

	console.log(selectFormFieldIds)

});





function insertSelectOptions(selectId, options){

    let select = document.getElementById(selectId)
    
    for (let el in options){

        select.options.add(new Option(options[el], options[el]))

    }

}

function createCheckboxes(){

    var form = document.getElementById('formId')

    options = [
        'Occurrence: General Liability',
        "Occurrence: Owners & Contractors Protective",
        "Claims Made: Products Liability",
        "Claims Made: Life Sciences Liability",
        'Excess Claims Made: Products Liability',
        'Limit Damage to Premises Rented to You',
        'Each Common Cause Liquor Liability',
        'Limit Products / Completed Operations Aggregate',
        'Per Occurrence Coverage Limits',
        'General Aggregate Coverage Limits',
        'Limit Personal / Advertising Injury',
        'Limit Medical Expense',
        'Limit Per Project Aggregate',
        'Each Employee Employee Benefits Liability',
        'Limit Per Location Aggregate',
        'Employee Benefits Liability',
        'Assault & Battery',
        'Hired / Non-Owned Auto Liability',
        'Liquor Liability',
        'Data Breach',
        'Other',
        'Per Claim Limit Coverage Limits',
        'Coverage Premium',
        'Terrorism'
    ]

    for (let option in options){
        // console.log(options[option])
        let div = document.createElement('div');
        div.classList.add('form-check')

        let checkboxString = document.createElement('input')
        checkboxString.type = 'checkbox'
        checkboxString.value = ''
        checkboxString.id = options[option]
        checkboxString.classList.add('form-check-input')

        div.appendChild(checkboxString)

        let label = document.createElement('label');
        label.classList.add('form-check-label')
        label.htmlFor = options[option]
        label.innerText = options[option]

        div.appendChild(label)

        form.insertBefore(div, form.childNodes[form.childNodes.length - 2])
    }
}

function submitForm(){
    formValues = []


    selectFormFieldIds = Array.from(document.getElementById('formId')
                              .getElementsByTagName('select'))
                              .map(el => el.id)

    // Select fields
    for (let selectId in selectFormFieldIds){
        let id = selectFormFieldIds[selectId]
        selectField = document.getElementById(id)

        formValues.push(selectFormFieldIds[selectId] + "_" + selectField.options[selectField.selectedIndex].value)
    }

    // console.log(formValues)

    checkboxes = Array.from(document.getElementById('formId')
                              .getElementsByTagName('input'))
                              .map(el => el.id)

    // Checkboxes:
    for (let checkid in checkboxes){
        let checkbox = document.getElementById(checkboxes[checkid])
        if (checkbox.checked)
            formValues.push(checkboxes[checkid])
    }

    console.log(formValues)

	$("#my_gif").show();
	console.log('WRITE')
    $.ajax({
		url: "/postforms",
		type: "POST",
		data: JSON.stringify({x: formValues}),
		contentType: "application/json; charset=utf-8",
		success: function(dat) {
		console.log(dat);
		 }
	}).done(function(){
		$.ajax({
			url: "http://localhost:5000/sendinfo",
			type: 'GET',
			dataType: 'json', // added data type,
			success: function(res) {
				console.log(res);
				forms_res = res.list_of_data
				$("#my_gif").hide();
			}
		}).done(function(){
			document.getElementById("list").innerHTML = "";
			for (el in forms_res){
   			  var ul = document.getElementById("list");
			  var li = document.createElement("li");
			  li.appendChild(document.createTextNode(forms_res[el]));
			  ul.appendChild(li);
			 }
		});
    });

	return formValues

}