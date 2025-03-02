import axios, { AxiosInstance } from "axios";

export class Api {
  public api: AxiosInstance;

  constructor(base_url: string) {
    const api_url = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
    this.api = axios.create({
      baseURL: `${api_url}${base_url}`,
      headers: {
        "Content-Type": "application/json",
      },
    });
  }
}
