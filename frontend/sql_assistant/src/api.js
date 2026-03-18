import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

export const fetchQuery = async (question) => {
  try {
    const res = await axios.post(`${API_URL}/query`, { question });
    return res.data;
  } catch (err) {
    console.error("API error:", err);
    throw err;
  }
};