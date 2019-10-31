//other
const isObject = data => {
  return data instanceof Object && !(data instanceof Array)
}

const isHasKey = (data, key) => {
  return isObject(data) && key in data;
};

const isEmpty = obj => !Object.keys(obj).length;


//normalizes
const normalizesFormObj = formObj => {
  let normFormObj = {};
  for (let dataKey in formObj) {
    let name = formObj[dataKey].name;
    if (name === undefined) {
      normFormObj[dataKey] = formObj[dataKey];
      continue;
    }

    if (formObj[dataKey].type === 'file') {
      normFormObj[name] = formObj[dataKey].file
    } else {
      if (formObj[dataKey].value === null) {
        formObj[dataKey].value = '';
      } else {
        normFormObj[name] = formObj[dataKey].value
      }
    }

    let clear = formObj[dataKey].clear;
    if (!(clear === null || clear === undefined)) {
      normFormObj[`clear_${name}`] = formObj[dataKey].clear;
    }
  }
  return normFormObj
}



//create
const createFormObj = ({
  name,
  label = "",
  prependIcon = "",
  type = "text",
  file = '',
  autofocus = false,
  required = false,
  clear = null,
  value = "",
  errors = []
}) => {
  //arg: {name: 'name', value: 'value,...}
  return {
    name: name,
    label: label,
    prependIcon: prependIcon,
    type: type,
    file: file,
    autofocus: autofocus,
    required: required,
    clear: clear,
    value: value,
    errors: errors,
  };
};

function createThatFormObj(that, argObj) {
  const formObj = createFormObj(argObj);
  that.$set(that.formObj, formObj['name'], formObj);
};

function createThatFormObjs(that, ...argObjs) {
  for (let argObj of argObjs) {
    const formObj = createFormObj(argObj);
    that.$set(that.formObj, formObj['name'], formObj);
  }
};

const createFormData = formObj => {
  let normFormObj = normalizesFormObj(formObj)
  let formData = new FormData();
  for (let dataKey in normFormObj) {
    formData.append(dataKey, normFormObj[dataKey])
  }
  return formData
}


//assign
function assignThatErrors(that, errors) {
  const formObj = that.formObj;
  assignErrors(formObj, errors);
};

function assignDataToThatObj(that, data) {
  assignDataToObj(that.formObj, data);
};

const assignDataToObj = (obj, data) => {
  for (let dataKey in data) {
    let isUndefined = obj[dataKey] === undefined
    if (!(isUndefined)) {
      obj[dataKey].value = data[dataKey]
    }
  }
}
const assignErrors = (formObj, errors) => {
  for (let errorKey in errors) {
    formObj[errorKey].errors = errors[errorKey];
  }
}



//set
const setFileToThatFormObj = (form, file) => {
  if (file === null) {
    form.file = '';
    return
  } 
  const fileReader = new FileReader();

  fileReader.onload = function() {
    form.value = this.result;
    form.file = file;
  }
  fileReader.readAsDataURL(file);
}


//claer
const clearErrors = (formObj) => {
  for (let formKey in formObj) {
    formObj[formKey].errors = [];
  } 
}



const FormHelper = {
  isEmpty,
  normalizesFormObj,
  createFormData,
  assignDataToThatObj,
  createThatFormObj,
  createThatFormObjs,
  assignErrors,
  clearErrors,
  assignThatErrors,
  setFileToThatFormObj,
  isEmpty,
}

export default FormHelper