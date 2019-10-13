export const dateToJapan = date => {
  if (!date) return null;

  const year = date.slice(0, 4);
  const month = date.slice(5, 7);
  const day = date.slice(8, 10);
  return `${year}年${month}月${day}日`;
};

export const datetimeToJapan = datetime => {
  if (!datetime) return null;
  const dt = new Date(datetime);
  return dt.toLocaleString();
} 