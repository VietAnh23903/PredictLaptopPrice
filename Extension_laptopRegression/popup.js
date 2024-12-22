document.getElementById("dudoan").addEventListener("click", () => {
 
  // Lấy giá trị từ các textbox
  const ram = document.getElementById("ram").value;
  const manhinh = document.getElementById("manhinh").value;
  const ocung = document.getElementById("ocung").value+' '+document.getElementById("type").value;

  // Kiểm tra nếu người dùng chưa nhập giá trị
  // if (!ram || !manhinh || !ocung) {
  //     alert("Vui lòng nhập đầy đủ thông tin!");
  //     return;
  // }
  const selectedText = "Ram "+ram+" Màn hình "+manhinh+" Ổ cứng: "+ocung;
  // Hiển thị thông tin trong alert
   // fetch("http://127.0.0.1:5000/api/du_bao_gia", {
  //   method: "POST", // Đúng phương thức
  //   headers: {
  //     "Content-Type": "application/json"
  //   },
  //   body: JSON.stringify({ text: selectedText })
  // })
  alert(selectedText);
});