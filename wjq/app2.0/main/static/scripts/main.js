// 获取元素
const searchForm = document.getElementById('search-form');
const queryInput = document.getElementById('query');
const directoryInput = document.getElementById('directory_path');
const resultsTableBody = document.querySelector('#results tbody');
const saveButton = document.getElementById('save-button');
const downloadLink = document.getElementById('download-link');

// 选择文件夹
function selectDirectory() {
  window.api.send('selectDirectory', '');
}

// 检索文件
async function searchFiles(event) {
  event.preventDefault();
  const query = queryInput.value;
  const directoryPath = directoryInput.value;
  const response = await fetch('/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      query,
      directoryPath
    })
  });
  const data = await response.json();
  updateResultsTable(data);
  saveButton.disabled = false;
}

// 更新检索结果表格
function updateResultsTable(results) {
  resultsTableBody.innerHTML = '';
  if (results.length === 0) {
    resultsTableBody.innerHTML = '<tr><td colspan="4">没有找到匹配项</td></tr>';
  } else {
    for (let i = 0; i < results.length; i++) {
      const result = results[i];
      const row = document.createElement('tr');
      const selectCell = document.createElement('td');
      const selectCheckbox = document.createElement('input');
      selectCheckbox.type = 'checkbox';
      selectCheckbox.checked = true;
      selectCell.appendChild(selectCheckbox);
      row.appendChild(selectCell);
      const pathCell = document.createElement('td');
      pathCell.textContent = result['file_path'];
      row.appendChild(pathCell);
      const lineNumCell = document.createElement('td');
      lineNumCell.textContent = result['lines'][0]['line_number'];
      row.appendChild(lineNumCell);
      const lineTextCell = document.createElement('td');
      lineTextCell.textContent = result['lines'][0]['line_text'];
      row.appendChild(lineTextCell);
      resultsTableBody.appendChild(row);
    }
  }
}

// 保存检索结果到文件
async function saveResults(event) {
  event.preventDefault();
  const selectedRows = Array.from(resultsTableBody.querySelectorAll('tr'))
    .filter(row => row.querySelector('input[type="checkbox"]').checked);
  const data = selectedRows.map(row => {
    const path = row.querySelector('td:nth-child(2)').textContent;
    const lineNum = row.querySelector('td:nth-child(3)').textContent;
    const lineText = row.querySelector('td:nth-child(4)').textContent;
    return { path, lineNum, lineText };
  });
  const response = await fetch('/download', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      data
    })
  });
  const blob = await response.blob();
  downloadLink.href = URL.createObjectURL(blob);
  downloadLink.click();
}

// 监听事件
searchForm.addEventListener('submit', searchFiles);
saveButton.addEventListener('click', saveResults);
