import axios from "axios";

const api = axios.create({
  baseURL: "https://file-parshing.onrender.com",
});

export default api;