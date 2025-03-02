import { Api } from ".";
import { DashboardMetrics } from "../../interfaces/dashboard";

export class DashboardApi extends Api {
  constructor() {
    super("/dashboard");
  }

  async getMetrics(
    startDate: Date | null,
    endDate: Date | null,
  ): Promise<DashboardMetrics> {
    const params: Record<string, string> = {};

    if (startDate !== null) {
      params["start_date"] = startDate.toISOString().split("T")[0];
    }

    if (endDate !== null) {
      params["end_date"] = endDate.toISOString().split("T")[0];
    }

    const { data } = await this.api.get<DashboardMetrics>("", { params });

    return data;
  }
}

export const dashboardApi = new DashboardApi();
