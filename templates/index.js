
const url = ''

createCheckboxes()

selectFormFieldIds = Array.from(document.getElementById('formId')
                             .getElementsByTagName('select'))
                             .map(el => el.id)

console.log(selectFormFieldIds)

fetchSelectOptions(selectFormFieldIds)

function fetchSelectOptions(selectFields) {

    for (let fieldName in selectFields){

        console.log(selectFields[fieldName])
        insertSelectOptions(selectFields[fieldName], ['opt1', 'opt2'])

        // fetch('http://www.google.com')
        //     .then(res => {
        //         res.json()
        //             .then(json => {

        //             })
        //             .catch(err => console.log(err))
        //     })
        //     .catch(err => {
        //         insertSelectOptions("BusinessSegment", ['opt1', 'opt2', 'opt3'])
        //     })
    }

}

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

    return formValues

}