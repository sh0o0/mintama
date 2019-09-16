const isObjAndHasKey = (data, key) => {
  return data instanceof Object && !(data instanceof Array) && key in data;
};

export const normalizesFormData = datasObj => {
  const normalizedData = new FormData();
  for (let dataKey in datasObj) {
    if (isObjAndHasKey(datasObj[dataKey], "value")) {
      if (dataKey === "icon" && typeof datasObj[dataKey].value === "string")
        continue;
      normalizedData.append(dataKey, datasObj[dataKey].value);
    } else {
      if (dataKey === "icon" && typeof datasObj[dataKey] === "string")
      continue;
      normalizedData.append(dataKey, datasObj[dataKey]);
    }
  }
  return normalizedData;
};

export const setErrors = (datasObj, errors) => {
  for (let dataKey in errors) {
    console.log(dataKey)
    datasObj[dataKey].errors = errors[dataKey];
  }
};
