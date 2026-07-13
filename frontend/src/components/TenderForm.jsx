import React from "react";
import { useForm } from "react-hook-form";
import api from "../services/api";

const defaultValues = {
  tender_id: "",
  tender_reference_no: "",
  authority_name: "",
  authority_type: "",
  department: "",
  tender_title: "",
  tender_description: "",
  tender_type: "",
  tender_category: "",
  procurement_type: "",
  sector: "",
  contract_type: "",
  state_ut: "",
  district: "",
  tender_publish_date: "",
  document_download_start: "",
  document_download_end: "",
  submission_start_date: "",
  submission_deadline: "",
  bid_open_date: "",
  delivery_period: "",
  bid_validity: "",
  currency: "",
  emd_amount: "",
  emd_type: "",
  tender_fee: "",
  tender_fee_payment_mode: "",
  submission_mode: "",
  mandatory_documents: "",
  document_submission_mode: "",
  evaluation_method: "",
  disqualification_clauses: "",
};

const fields = [
  ["tender_id", "Tender ID"],
  ["tender_reference_no", "Tender Reference No"],
  ["authority_name", "Authority Name"],
  ["authority_type", "Authority Type"],
  ["department", "Department"],
  ["tender_title", "Tender Title"],
  ["tender_description", "Tender Description", "textarea"],
  ["tender_type", "Tender Type"],
  ["tender_category", "Tender Category"],
  ["procurement_type", "Procurement Type"],
  ["sector", "Sector"],
  ["contract_type", "Contract Type"],
  ["state_ut", "State / UT"],
  ["district", "District"],
  ["tender_publish_date", "Tender Publish Date"],
  ["document_download_start", "Document Download Start"],
  ["document_download_end", "Document Download End"],
  ["submission_start_date", "Submission Start Date"],
  ["submission_deadline", "Submission Deadline"],
  ["bid_open_date", "Bid Open Date"],
  ["delivery_period", "Delivery Period"],
  ["bid_validity", "Bid Validity"],
  ["currency", "Currency"],
  ["emd_amount", "EMD Amount"],
  ["emd_type", "EMD Type"],
  ["tender_fee", "Tender Fee"],
  ["tender_fee_payment_mode", "Tender Fee Payment Mode"],
  ["submission_mode", "Submission Mode"],
  ["mandatory_documents", "Mandatory Documents", "textarea"],
  ["document_submission_mode", "Document Submission Mode"],
  ["evaluation_method", "Evaluation Method"],
  ["disqualification_clauses", "Disqualification Clauses", "textarea"],
];

export default function TenderForm({ extractedData }) {
  const { register, reset, handleSubmit } = useForm({ defaultValues });
  const [saving, setSaving] = React.useState(false);
  const [msg, setMsg] = React.useState("");

  React.useEffect(() => {
    if (extractedData) reset({ ...defaultValues, ...extractedData });
  }, [extractedData, reset]);

  const onSubmit = async (data) => {
    setSaving(true);
    setMsg("");
    try {
      const r = await api.post("/documents", data);
      setMsg(r.data.message || "Document saved successfully.");
    } catch (e) {
      setMsg(e.response?.data?.message || "Failed to save document.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <div className="border-b pb-4 mb-6">
        <h2 className="text-2xl font-bold">Tender Details</h2>
        <p className="text-slate-500">
          Review and edit extracted information before saving.
        </p>
      </div>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {fields.map(([n, l, t]) => (
            <div key={n} className={t === "textarea" ? "md:col-span-2" : ""}>
              <label className="block mb-2 font-semibold">{l}</label>
              {t === "textarea" ? (
                <textarea
                  rows={4}
                  {...register(n)}
                  className="w-full rounded-xl border p-3"
                />
              ) : (
                <input
                  {...register(n)}
                  className="w-full rounded-xl border p-3"
                />
              )}
            </div>
          ))}
        </div>
        <div className="mt-8 flex gap-4 items-center">
          <button
            type="submit"
            disabled={saving}
            className="bg-blue-600 text-white px-8 py-3 rounded-xl"
          >
            {saving ? "Saving..." : "Save Document"}
          </button>
          {msg && <div>{msg}</div>}
        </div>
      </form>
    </div>
  );
}
