const dateToJp = date => {
  if (!date) return null;

  const year = date.slice(0, 4);
  const month = date.slice(5, 7);
  const day = date.slice(8);
  return `${year}年${month}月${day}日`;
};

export default {
  dateToJp
}