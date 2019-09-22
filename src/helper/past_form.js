const isHasKey = (data, key) => {
  return data instanceof Object && !(data instanceof Array) && key in data;
};

const takeoutFormData = dataObj => {
  //arg: {name: 'name', value: 'value,...}
  for (let dataKey in dataObj) {
    if (isHasKey(dataObj[dataKey], "value")) {
      if (dataKey === "icon" && typeof dataObj[dataKey].value === "string") continue;
      normalizedData.append(dataKey, dataObj[dataKey].value);
    } else {
      if (dataKey === "icon" && typeof dataObj[dataKey] === "string") continue;
      normalizedData.append(dataKey, dataObj[dataKey]);
    }
  }
  return normalizedData;
};

const createFormData = () => {
  const normalizedData = new FormData();

}

const assignDataToObj = (clientDataObj, serverDataObj) => {
  for (let clientKey in clientDataObj) {
    if ( isHasKey(clientDataObj[clientKey], 'value')) {
      
      serverData= clientDataObj[clientKey]
    }
  }
}

const createFormObj = (
  name,
  value = "",
  errors = [],
  label = "",
  type = "text",
  clear = false,
  autofocus = false,
  required = false,
  prependIcon = ""
) => {
  return {
    name: name,
    value: value,
    errors: errors,
    type: type,
    clear: clear,
    label: label,
    autofocus: autofocus,
    required: required,
    prependIcon: prependIcon
  };
};



const setErrors = (datasObj, errors) => {
  for (let dataKey in errors) {
    console.log(dataKey);
    datasObj[dataKey].errors = errors[dataKey];
  }
};
