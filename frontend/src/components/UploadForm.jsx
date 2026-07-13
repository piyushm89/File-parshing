import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { UploadCloud, FileText, X, Loader2 } from "lucide-react";
import api from "../services/api";

function UploadForm({ setExtractedData }) {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      setError("");
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: false,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
    },
  });

  const removeFile = () => {
    setFile(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");

    if (!file && text.trim() === "") {
      setError("Please upload a document or paste text.");
      return;
    }

    const formData = new FormData();

    if (file) {
      formData.append("file", file);
    }

    if (text.trim()) {
      formData.append("text", text);
    }

    try {
      setLoading(true);

      const response = await api.post("/extract", formData);

      if (response.data.status === "error") {
        setError(response.data.message);
        return;
      }

      setExtractedData(response.data.data);

    } catch (err) {
      setError(
        err.response?.data?.message ||
          err.message ||
          "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">

      <div>
        <h2 className="text-2xl font-bold text-slate-800">
          Upload Tender Document
        </h2>

        <p className="text-slate-500 mt-2">
          Drag & Drop a document or click to browse.
        </p>
      </div>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition

        ${
          isDragActive
            ? "border-blue-600 bg-blue-50"
            : "border-slate-300 hover:border-blue-500 hover:bg-slate-50"
        }`}
      >
        <input {...getInputProps()} />

        <UploadCloud className="mx-auto h-14 w-14 text-blue-600 mb-4" />

        <h3 className="text-lg font-semibold">
          Drag & Drop your document here
        </h3>

        <p className="text-slate-500 mt-2">
          or click to browse
        </p>

        <p className="text-sm text-gray-400 mt-4">
          Supported formats: PDF • DOCX • XLSX
        </p>
      </div>

      {file && (
        <div className="flex items-center justify-between bg-green-50 border border-green-200 rounded-xl p-4">

          <div className="flex items-center gap-3">

            <FileText className="text-green-600" />

            <div>

              <p className="font-medium">{file.name}</p>

              <p className="text-sm text-gray-500">
                {(file.size / 1024).toFixed(2)} KB
              </p>

            </div>

          </div>

          <button
            type="button"
            onClick={removeFile}
            className="text-red-500 hover:text-red-700"
          >
            <X />
          </button>

        </div>
      )}

      <div className="text-center text-gray-400 font-semibold">
        OR
      </div>

      <div>

        <label className="block font-medium mb-2">
          Paste Tender Text
        </label>

        <textarea
          rows={7}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste tender text here..."
          className="w-full rounded-xl border border-slate-300 p-4 focus:ring-2 focus:ring-blue-500 outline-none resize-none"
        />

      </div>

      {error && (
        <div className="rounded-xl bg-red-100 border border-red-300 text-red-700 p-4">
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 transition text-white font-semibold py-3 rounded-xl disabled:bg-gray-400"
      >
        {loading && (
          <Loader2 className="animate-spin h-5 w-5" />
        )}

        {loading ? "Extracting..." : "Extract Document"}
      </button>

    </form>
  );
}

export default UploadForm;