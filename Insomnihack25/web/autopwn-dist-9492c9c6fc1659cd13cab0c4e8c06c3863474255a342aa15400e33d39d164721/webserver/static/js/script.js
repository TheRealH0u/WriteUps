(() => {
  "use strict";

  const resultDiv = document.getElementById("result-div");
  const resultContent = document.getElementById("result-content");
  const templateInput = document.getElementById("template-select");
  const scanButton = document.getElementById("scan-button");

  var scanRefreshInterval = null;

  const loadResults = (scanID) => {
    if (scanRefreshInterval) {
      clearInterval(scanRefreshInterval);
      scanRefreshInterval = null;
    }
    scanRefreshInterval = setInterval(() => {
      fetch("/scan/" + scanID)
        .then((response) => response.json())
        .then((data) => {
          if (data.logs) {
            resultContent.innerText = data.logs;
          }
          if (data.status === "completed") {
            clearInterval(scanRefreshInterval);
            scanRefreshInterval = null;
            scanning = false;
            scanButton.disabled = false;
          }
        });
    }, 2000);
  };

  let scanning = false;
  const scan = () => {
    if (scanning) {
      return;
    }
    scanning = true;
    scanButton.disabled = true;

    resultDiv.classList.add("invisible");
    resultContent.innerHTML = "";

    const template = templateInput.value;
    if (!template) {
      return;
    }

    fetch("/scan", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ template }),
    })
      .then((response) => response.json())
      .then((data) => {
        resultDiv.classList.remove("invisible");
        resultContent.innerText = JSON.stringify(data);
        if (data.task_id) {
          resultContent.innerText = "Scan started...";
          loadResults(data.task_id);
        }
      });
  };

  document.getElementById("scan-form").addEventListener("submit", (event) => {
    event.preventDefault();
    scan();
  });
})();
