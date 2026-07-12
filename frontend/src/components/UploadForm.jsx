import { useState } from "react";
import api from "../services/api";

function UploadForm({ setExtractedData }) {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");

    if (!file && text.trim() === "") {
      setError("Please upload a PDF/DOCX file or enter text.");
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

      const extracted = response.data.data;

      if (extracted?.status === "error") {
        setError(extracted.message || "Extraction failed.");
        return;
      }

      setExtractedData(extracted);

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

      {/* Heading */}
      <div>
        <h2 className="text-2xl font-bold text-slate-800">
          Upload Tender Document
        </h2>

        <p className="text-slate-500 mt-1">
          Upload a PDF/DOCX document or paste tender text for AI extraction.
        </p>
      </div>

      {/* Upload Box */}
      <div className="border-2 border-dashed border-blue-300 rounded-xl bg-blue-50 p-8 text-center">

        <input
          type="file"
          accept=".pdf,.docx"
          onChange={(e) => setFile(e.target.files[0])}
          className="block mx-auto cursor-pointer"
        />

        {file && (
          <div className="mt-4 rounded-lg bg-green-100 text-green-700 px-4 py-2 inline-block">
            📄 {file.name}
          </div>
        )}

      </div>

      {/* OR Divider */}
      <div className="flex items-center gap-4">

        <div className="flex-1 h-px bg-gray-300"></div>

        <span className="text-gray-500 font-medium">
          OR
        </span>

        <div className="flex-1 h-px bg-gray-300"></div>

      </div>

      {/* Text Area */}
      <div>

        <label className="block text-sm font-medium text-gray-700 mb-2">
          Paste Tender Text
        </label>

        <textarea
          rows="8"
          placeholder="Paste tender content here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="w-full rounded-lg border border-gray-300 p-4 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        />

      </div>

      {/* Error */}
      {error && (
        <div className="rounded-lg bg-red-100 border border-red-300 text-red-700 px-4 py-3">
          {error}
        </div>
      )}

      {/* Extract Button */}
      <button
        type="submit"
        disabled={loading}
        className={`w-full py-3 rounded-lg font-semibold text-white transition duration-200 ${
          loading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700"
        }`}
      >
        {loading ? "Extracting..." : "Extract Document"}
      </button>

    </form>
  );
}

export default UploadForm;