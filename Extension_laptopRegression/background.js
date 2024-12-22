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
        
        // mã hóa text để giải mã bên phía server 
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
            // chrome.scripting.executeScript({
            //   target: { tabId: tab.id },
            //   func: () => {
            //     const loaderDiv = document.getElementById("loading-overlay");
            //     if (loaderDiv) loaderDiv.remove();
            //   }
            // });
            var check = data.check;
            var input = data.input_text;
            
            if(check == 1){
              var predictPrice = data.predicted_price;
              var mse = data.mse
              var r2= data.r2
              // Hiển thị kết quả trả về từ API
              chrome.scripting.executeScript({
                target: { tabId: tab.id },
                func: (input, predictPrice, mse, r2) => {
                  alert(`Dữ liệu đầu vào: ${JSON.stringify(input, null, 2)}\n
                    Giá laptop dự đoán: ${predictPrice} VND\n 
                    MSE: ${mse}\n
                    R2: ${r2}`);
                },
                args: [input, predictPrice, mse, r2]
              });
            }
            else{
              chrome.scripting.executeScript({
                target: { tabId: tab.id },
                func: (result) => {
                  alert(`${result}`);
                },
                args: [input]
              });
            }
            
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
  