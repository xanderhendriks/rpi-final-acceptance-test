export const createCSV = (data: any[], filename: string) => {
  const csvContent =
    'data:text/csv;charset=utf-8,' + data.map(row => row.join(',')).join('\n');
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement('a');
  link.setAttribute('href', encodedUri);
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
