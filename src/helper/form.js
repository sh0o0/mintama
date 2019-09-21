const isHasKey = (data, key) => {
  return data instanceof Object && !(data instanceof Array) && key in data;
};

const normalizesFormObj = formObj => {
  let normFormObj = {};
  for (let dataKey in formObj) {
    let name = formObj[dataKey].name;
    if (!(name === undefined)) {
      if (formObj[dataKey].type === 'file') {
        //image objectを格納
        normFormObj[name] = formObj[dataKey].image
      } else {
        normFormObj[name] = formObj[dataKey].value
      }
      normFormObj[`clear_${name}`] = formObj[dataKey].clear;
    } else {
      normFormObj[dataKey] = formObj[dataKey]
    }
  }
  return normFormObj
}

const createFormData = normFormObj => {
  console.log(normFormObj)
  let formData = new FormData();
  for (let dataKey in normFormObj) {
    formData.append(dataKey, normFormObj[dataKey])
  }
  //test
  formData.append('icon_clear', false)
  formData.append('icon', '')
  return formData
}
// const createFormData = formObj => {
//   const normFormObj = normalizesFormObj(formObj);
//   let formData = new FormData();
//   for (let dataKey in normFormObj) {
//     formData.append(normFormObj[dataKey])
//   }
//   return formData
// }

const assignDataToObj = (data, obj) => {
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

const createFormObj = ({
  name,
  label = "",
  prependIcon = "",
  type = "text",
  file = null,
  autofocus = false,
  required = false,
  clear = false,
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

// function assignDataToObjForCall(data) {
//   const obj = this.formObj;
//   assignDataToObj(data, obj);
// };

// function createFormObjForCall(argObj) {
//   const formObj = createFormObj(argObj);
//   this.$set(this.formObj, formObj['name'], formObj);
// };

// function createFormObjsForCall(...argObjs) {
//   for (let argObj in argObjs) {
//     const formObj = createFormObj(argObj);
//     this.$set(this.formObj, formObj['name'], formObj);
//   }
// };

// function assignErrorsForCall(errors) {
//   const formObj = this.formObj;
//   assignErrors(formObj, errors);
// };


function assignDataToThatObj(that, data) {
  const obj = that.formObj;
  assignDataToObj(data, obj);
};

function createThatFormObj(that, argObj) {
  const formObj = createFormObj(argObj);
  that.$set(that.formObj, formObj['name'], formObj);
};

function createThatFormObjs(that, ...argObjs) {
  for (let argObj in argObjs) {
    const formObj = createFormObj(argObj);
    that.$set(that.formObj, formObj['name'], formObj);
  }
};

function assignThatErrors(that, errors) {
  const formObj = that.formObj;
  assignErrors(formObj, errors);
};

const setFileToThatFormObj = (that, formName, file) => {
  const fileReader = new FileReader();

  fileReader.onload = () => {
    that.formObj[formName].value = this.result;
    that.formObj[formName].file = fileObj;
  }
  fileReader.readAsDataURL(file);
}


const FormHelper = {
  normalizesFormObj,
  createFormData,
  assignDataToThatObj,
  createThatFormObj,
  createThatFormObjs,
  assignThatErrors,
  setFileToThatFormObj,
}

export default FormHelper