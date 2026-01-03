const dropzone = document.getElementById("dropzone");

dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
      dropzone.classList.add("hover");
});

dropzone.addEventListener("drop", async (e) => {
  e.preventDefault();
      dropzone.classList.remove("hover");

dropzone.addEventListener("drop", async (e) => {
    e.preventDefault();
    dropzone.classList.remove("hover");

  const file = e.dataTransfer.files[0];
     if (!file) return;
  const formData = new FormData();
  formData.append("file", file);
try {
  const response = await fetch("/upload", {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
      const text = await response.text();
      console.error("Upload fehlgeschlagen:", response.status, text);
            return;
        }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "rechnung.pdf";
  document.body.appendChild(a);
        a.click();
        a.remove();
    } catch (err) {
        console.error(err);
    }
});


