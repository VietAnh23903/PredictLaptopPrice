chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
      id: "processText",
      title: "Dự báo giá!",
      contexts: ["selection"] // Chỉ hiển thị khi bôi đen văn bản
    });
  });
  
  // chrome.contextMenus.onClicked.addListener((info, tab) => {
  //   if (info.menuItemId === "processText") {
  //     const selectedText = info.selectionText;
  //     if (selectedText) {
  //       chrome.scripting.executeScript({
  //         target: { tabId: tab.id },
  //         func: (text) => {
  //           alert(`${text}`);
  //         },
  //         args: [selectedText],
  //       }).catch((error) => {
  //         console.error("Lỗi khi thực thi mã:", error);
  //       });
  //     } else {
  //       console.error("Không có đoạn văn bản nào được bôi đen.");
  //     }
  //   }
  // });
  chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "processText") {
      const selectedText = info.selectionText; // Lấy đoạn văn bản bôi đen
      if (selectedText) {
        // Chèn thông báo "Đang dự báo" với icon
        chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: () => {
            const loaderDiv = document.createElement("div");
            loaderDiv.id = "loading-overlay";
            loaderDiv.style.position = "fixed";
            loaderDiv.style.top = "0";
            loaderDiv.style.left = "0";
            loaderDiv.style.width = "100vw";
            loaderDiv.style.height = "100vh";
            loaderDiv.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
            loaderDiv.style.display = "flex";
            loaderDiv.style.alignItems = "center";
            loaderDiv.style.justifyContent = "center";
            loaderDiv.style.zIndex = "9999";
            loaderDiv.innerHTML = `
              <div style="text-align: center; color: white;">
                <div class="spinner" style="
                  width: 50px;
                  height: 50px;
                  border: 5px solid rgba(255, 255, 255, 0.3);
                  border-radius: 50%;
                  border-top-color: white;
                  animation: spin 1s ease-in-out infinite;
                "></div>
                <p>Đang dự báo...</p>
              </div>
              <style>
                @keyframes spin {
                  to {
                    transform: rotate(360deg);
                  }
                }
              </style>
            `;
            document.body.appendChild(loaderDiv);
          }
        });
        let encodedText = encodeURIComponent(selectedText)

        // Gửi đoạn văn bản đến API
        fetch("http://127.0.0.1:5000/api/du_bao_gia", {
          method: "POST", // Đúng phương thức
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ text: encodedText })
        })
          .then((response) => response.json())
          .then((data) => {
            // Xóa thông báo "Đang load"
            chrome.scripting.executeScript({
              target: { tabId: tab.id },
              func: () => {
                const loaderDiv = document.getElementById("loading-overlay");
                if (loaderDiv) loaderDiv.remove();
              }
            });
  
            // Hiển thị kết quả trả về từ API
            chrome.scripting.executeScript({
              target: { tabId: tab.id },
              func: (result) => {
                alert(`Kết quả xử lý: ${result}`);
              },
              args: [JSON.stringify(data)]
            });
          })
          .catch((error) => {
            console.error("Lỗi khi gọi API:", error);
  
            // Xóa thông báo "Đang load" nếu lỗi xảy ra
            chrome.scripting.executeScript({
              target: { tabId: tab.id },
              func: () => {
                const loaderDiv = document.getElementById("loading-overlay");
                if (loaderDiv) loaderDiv.remove();
                alert("Đã xảy ra lỗi khi gọi API.");
              }
            });
          });
      } else {
        console.error("Không có đoạn văn bản nào được bôi đen.");
      }
    }
  });
  