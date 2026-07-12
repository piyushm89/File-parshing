import { useState } from "react";
import UploadForm from "./components/UploadForm";
import TenderForm from "./components/TenderForm";

function App() {
  const [extractedData, setExtractedData] = useState(null);

  return (
    <div className="min-h-screen bg-slate-100">
      <div className="max-w-7xl mx-auto px-6 py-10">

        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold text-slate-800">
            AI Document Extraction & Content Tracking
          </h1>

          <p className="text-slate-600 mt-3">
            Upload a PDF, DOCX, or paste text to automatically extract tender information.
          </p>
        </div>

        {/* Upload Section */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <UploadForm setExtractedData={setExtractedData} />
        </div>

        {/* Tender Form */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <TenderForm extractedData={extractedData} />
        </div>

      </div>
    </div>
  );
}

export default App;