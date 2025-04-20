# My Project
第一版
 chart js健康監測網頁
![image](https://github.com/user-attachments/assets/8fa0829c-f514-439d-a5b8-6bbc73049234)

![image](https://github.com/user-attachments/assets/5c347ad9-8772-4cae-99d5-98dde714ba9d)

改良版 正常時笑臉 異常時怒臉
數據加上5種顏色 分明


![image](https://github.com/user-attachments/assets/ca38f258-9e0d-40ed-8877-ea7ff33ef332)


![image](https://github.com/user-attachments/assets/31bb1304-a767-4b83-82dc-2d693181e46e)


![image](https://github.com/user-attachments/assets/0e2937ce-2bb8-459a-a3f5-d544bb5cc425)

用於顯示一個健康監控系統的儀表板，並且利用 JavaScript 來更新和顯示即時數據。下面是對這個文部分的詳細解釋：

HTML 結構
<!DOCTYPE html> 和 <html> 標籤

定義文檔類型和根元素，設置語言為英文。
<head> 標籤

<meta charset="UTF-8">: 設置字符編碼為 UTF-8，支持多種語言字符。
<meta name="viewport" content="width=device-width, initial-scale=1.0">: 使頁面在移動設備上能夠自適應屏幕寬度。
<title>: 設置頁面的標題，顯示在瀏覽器的標籤上。
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>: 引入 Chart.js 庫，這是一個用於繪製圖表的 JavaScript 庫。
<style>: 定義內部樣式表，用於設計和定制頁面元素的樣式。
<body> 標籤

.container: 使用 Bootstrap 的容器類來設置響應式布局。
.title-with-image: 標題和圖標的容器，包含健康監控的標題和狀態圖標。
.banner-image: 健康監控的橫幅圖像，設置了最大寬度和自適應高度。
.row 和 .col-md-4: 使用 Bootstrap 的網格系統來布局三個主要的監控部分（環境身體監控、心跳、BMI）。
<canvas id="myChart">: 用於顯示歷史數據的 Chart.js 圖表。
<table>: 顯示歷史紀錄的表格，包含時間、數值、狀態和備註欄位。
.bottom-gif: 用於顯示頁面底部的動態 GIF。
JavaScript 功能
updateStatusImage(data)

根據提供的數據更新狀態圖標。如果所有數據都顯示正常，則顯示一個綠色的笑臉；否則顯示紅色的憂傷臉。
updateChart(heart_rate, BMI, temperature, body_temperature, humidity)

更新圖表數據。每次調用此函數時，它會向圖表添加新的數據點並更新顯示。圖表最多顯示 10 個數據點，超過的部分將被刪除。
updateData()

從伺服器端獲取最新數據，並根據這些數據更新頁面上的各個元素。包括更新溫度、濕度、體溫、心跳、BMI 和狀態，並調用 updateChart 和 updateHistoricalData 函數來更新圖表和歷史數據。
updateHistoricalData(historicalData)

更新歷史數據表格。清空現有的表格內容，並將新的歷史數據添加到表格中。
const ctx = document.getElementById('myChart').getContext('2d');

獲取圖表的上下文，以便可以使用 Chart.js 來繪製圖表。
const myChart = new Chart(ctx, {...})

創建一個新的 Chart.js 圖表實例。設置圖表的類型為線圖，並配置數據集和顯示選項。
setInterval(updateData, 2000);

每 2 秒調用一次 updateData 函數，以便定期更新數據。
CSS 樣式
.title-with-image: 設置標題和圖標的對齊方式。
.banner-image: 設置橫幅圖像的寬度和高度。
.icon-img: 設置圖標的大小和左邊距。
.bottom-gif: 設置底部動態 GIF 的大小和對齊方式。
小結
這段 HTML 文件結合了靜態頁面結構和動態數據更新功能。它利用 Chart.js 繪製健康監控數據圖表，通過定時更新從伺服器獲取的數據來保持信息的即時性。頁面使用了 Bootstrap 的網格系統來進行布局設計，並用自定義的 CSS 來設計頁面元素的樣式。




🧱 一、HTML（網頁骨架）
HTML 是「網頁內容的基本結構」，你可以把它想成房子的 鋼筋水泥結構。

在這份 HTML 裡：

<div class="card">...</div> 是每一個「健康資訊區塊」

<form id="riskForm">...</form> 是心臟病風險的「使用者輸入表單」

<table> 是「歷史紀錄表格」

<canvas> 是用來顯示圖表的畫布

👉 HTML 幫你定義：有哪些內容、文字、表單欄位 等。

🎨 二、Bootstrap（網頁美化 + 響應式排版）
Bootstrap 是一套「前端 UI 框架」，它幫你快速做出 漂亮又響應式（手機、平板、電腦自動調整） 的排版。

在你這份頁面中：

class="container"、class="row"、class="col-md-4"：這些是 Bootstrap 的網格系統，幫你把卡片區塊平均分成三欄。

class="form-control"、class="btn btn-primary"：這些是 Bootstrap 幫你設計的輸入框、按鈕樣式。

整個畫面都整齊美觀，得歸功於 Bootstrap。

👉 Bootstrap 幫你定義：排版、配色、樣式、響應式佈局。

⚙️ 三、jQuery（資料互動）
jQuery 是 JavaScript 的一個輕量級函式庫，它讓你寫 JS 更簡潔。你用 jQuery 來做的事包括：

✅ AJAX 表單送出（心臟病預測）
js
複製
編輯
$('#riskForm').on('submit', function(event) {
    // 送資料到後端 /predict，然後顯示預測結果
});
✅ 每 2 秒抓一次健康數據（AJAX 實時更新）
js
複製
編輯
setInterval(updateData, 2000); // 每兩秒抓一次 /get_latest_data 的資料
✅ DOM 操作：改變 HTML 元素內容
js
複製
編輯
$('#prediction-text').html(`預測結果：...`);
👉 jQuery 幫你做：和伺服器互動（AJAX）、修改畫面內容、處理事件點擊。

總結小表格 🧩

技術	用途	你這頁裡的功能
HTML	結構、內容	表單、卡片、表格、圖片
Bootstrap	美化、排版、響應式	三欄排版、按鈕樣式、表單
jQuery	前端互動、AJAX 非同步請求	自動更新資料、提交預測表單、顯示結果

