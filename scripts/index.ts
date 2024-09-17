import axios from "axios";
import fs from "fs";
import FormData from "form-data";

async function main() {
  async function uploadFile(filePath: string) {
    const formData = new FormData();
    // formData.append("file_input", fs.createReadStream(filePath), filePath);
    formData.append("file_input", fs.createReadStream(filePath));

    return axios.post("http://localhost:8088/uploadfile", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        accept: "application/json",
      },
      timeout: 500000, // Optional: Set a timeout for each request
    });
  }

  const final: any = [];

  async function uploadFiles(filePaths: string[]) {
    try {
      const uploadPromises = filePaths.map((filePath) => uploadFile(filePath));
      const responses = await axios.all(uploadPromises);
      responses.forEach((response) => {
        final.push(...response.data);
      });
    } catch (error) {
      console.error("Error uploading files:", error);
    }
  }

  // Example usage
  let filePaths: any = [];
  for (let i = 0; i < 4000; i++) {
    filePaths.push(`../output/document-${i}.pdf`);
  }

  let res: any = await uploadFiles(filePaths);

  filePaths = [];
  for (let i = 4000; i < 8000; i++) {
    filePaths.push(`../output/document-${i}.pdf`);
  }

  res = await uploadFiles(filePaths);

  filePaths = [];
  for (let i = 8000; i < 12028; i++) {
    filePaths.push(`../output/document-${i}.pdf`);
  }

  res = await uploadFiles(filePaths);


  // Write the final result to a file
  fs.writeFileSync("final.json", JSON.stringify(final, null, 2));
}

main();
