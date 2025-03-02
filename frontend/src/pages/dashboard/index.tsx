import React, { useState, useEffect } from "react";
import {
  Container,
  Grid2 as Grid,
  Paper,
  Typography,
  Box,
  CircularProgress,
  Card,
  CardContent,
} from "@mui/material";
import { DatePicker } from "@mui/x-date-pickers";
import { BarChart, LineChart, PieChart } from "@mui/x-charts";
import { DashboardMetrics } from "../../interfaces/dashboard";
import { dashboardApi } from "../../services/api/dashboard";

interface ChartData {
  ordersByPeriod: {
    date: string;
    count: number;
    revenue: number;
  }[];
  topProducts: {
    name: string;
    value: number;
  }[];
  revenueByCategory: {
    id: string;
    value: number;
    label: string;
  }[];
}

interface MetricCardProps {
  title: string;
  value: number;
  unit: "currency" | "number";
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, unit }) => (
  <Card elevation={2} sx={{ height: "100%" }}>
    <CardContent>
      <Typography variant="h6" color="text.secondary" gutterBottom>
        {title}
      </Typography>
      <Typography variant="h4" component="div">
        {unit === "currency"
          ? `R$ ${Number(value).toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
          : Number(value).toLocaleString("pt-BR", { maximumFractionDigits: 0 })}
      </Typography>
    </CardContent>
  </Card>
);

export default function DashboardPage() {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);
  const [chartData, setChartData] = useState<ChartData | null>(null);

  useEffect(() => {
    const loadMetrics = async () => {
      setLoading(true);
      try {
        const data = await dashboardApi.getMetrics(startDate, endDate);
        setMetrics(data);
        setError(null);

        prepareChartData(data);
      } catch (err) {
        console.error("Error fetching metrics:", err);
        setError("Unable to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };

    loadMetrics();
  }, [startDate, endDate]);

  const prepareChartData = (data: DashboardMetrics) => {
    const ordersByPeriodData = Object.entries(data.orders_by_period)
      .map(([date, data]) => ({
        date,
        count: data.count,
        revenue: data.revenue,
      }))
      .sort((a, b) => a.date.localeCompare(b.date));

    const topProductsData = data.top_products.map((product) => ({
      name: product.product_name,
      value: product.count,
    }));

    const revenueByCategoryData = data.revenue_by_category.map((category) => ({
      id: category.category_id,
      value: category.revenue,
      label: category.category_name,
    }));

    setChartData({
      ordersByPeriod: ordersByPeriodData,
      topProducts: topProductsData,
      revenueByCategory: revenueByCategoryData,
    });
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Sales Dashboard
      </Typography>

      <Box display="flex" gap={2} mb={4}>
        <DatePicker
          label="Start date"
          value={startDate}
          onChange={setStartDate}
          slotProps={{ textField: { variant: "outlined", fullWidth: true } }}
        />
        <DatePicker
          label="End date"
          value={endDate}
          onChange={setEndDate}
          slotProps={{ textField: { variant: "outlined", fullWidth: true } }}
        />
      </Box>

      {loading ? (
        <Box display="flex" justifyContent="center" mt={8}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Paper sx={{ p: 3, textAlign: "center", mt: 2 }}>
          <Typography color="error">{error}</Typography>
        </Paper>
      ) : metrics && chartData ? (
        <>
          <Grid container spacing={3} mb={4}>
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
              <MetricCard
                title="Total Orders"
                value={metrics.total_orders}
                unit="number"
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
              <MetricCard
                title="Average Ticket"
                value={metrics.average_order_value}
                unit="currency"
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
              <MetricCard
                title="Total Revenue"
                value={metrics.total_revenue}
                unit="currency"
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
              <MetricCard
                title="Orders per Day"
                value={
                  chartData.ordersByPeriod.length > 0
                    ? metrics.total_orders / chartData.ordersByPeriod.length
                    : 0
                }
                unit="number"
              />
            </Grid>
          </Grid>

          <Grid container spacing={3}>
            <Grid size={{ xs: 12, md: 8 }}>
              <Paper
                elevation={3}
                sx={{
                  p: 2,
                  display: "flex",
                  flexDirection: "column",
                  height: 350,
                }}
              >
                <Typography variant="h6" gutterBottom>
                  Sales by Period
                </Typography>
                {chartData.ordersByPeriod.length > 0 ? (
                  <LineChart
                    xAxis={[
                      {
                        data: chartData.ordersByPeriod.map((item) => item.date),
                        scaleType: "band",
                        label: "Date",
                      },
                    ]}
                    series={[
                      {
                        data: chartData.ordersByPeriod.map(
                          (item) => item.revenue,
                        ),
                        label: "Revenue (R$)",
                        curve: "natural",
                      },
                    ]}
                    height={280}
                  />
                ) : (
                  <Box
                    display="flex"
                    justifyContent="center"
                    alignItems="center"
                    height="100%"
                  >
                    <Typography color="text.secondary">
                      No data for the selected period
                    </Typography>
                  </Box>
                )}
              </Paper>
            </Grid>

            <Grid size={{ xs: 12, md: 4 }}>
              <Paper
                elevation={3}
                sx={{
                  p: 2,
                  display: "flex",
                  flexDirection: "column",
                  height: 350,
                }}
              >
                <Typography variant="h6" gutterBottom>
                  Revenue by Category
                </Typography>
                {chartData.revenueByCategory.length > 0 ? (
                  <PieChart
                    series={[
                      {
                        data: chartData.revenueByCategory,
                        innerRadius: 30,
                        outerRadius: 100,
                        paddingAngle: 2,
                        cornerRadius: 5,
                        startAngle: -90,
                        endAngle: 270,
                      },
                    ]}
                    height={280}
                    margin={{ right: 5 }}
                    slotProps={{
                      legend: { hidden: true },
                    }}
                  />
                ) : (
                  <Box
                    display="flex"
                    justifyContent="center"
                    alignItems="center"
                    height="100%"
                  >
                    <Typography color="text.secondary">
                      No data for the selected period
                    </Typography>
                  </Box>
                )}
              </Paper>
            </Grid>

            <Grid size={{ xs: 12 }}>
              <Paper
                elevation={3}
                sx={{
                  p: 2,
                  display: "flex",
                  flexDirection: "column",
                  height: 400,
                }}
              >
                <Typography variant="h6" gutterBottom>
                  Top 5 Products
                </Typography>
                {chartData.topProducts.length > 0 ? (
                  <BarChart
                    xAxis={[
                      {
                        scaleType: "band",
                        data: chartData.topProducts.map((item) => item.name),
                        label: "Product",
                      },
                    ]}
                    series={[
                      {
                        data: chartData.topProducts.map((item) => item.value),
                        label: "Order Quantity",
                      },
                    ]}
                    height={330}
                    margin={{
                      left: 80,
                      bottom: 70,
                    }}
                  />
                ) : (
                  <Box
                    display="flex"
                    justifyContent="center"
                    alignItems="center"
                    height="100%"
                  >
                    <Typography color="text.secondary">
                      No data for the selected period
                    </Typography>
                  </Box>
                )}
              </Paper>
            </Grid>

            <Grid size={{ xs: 12 }}>
              <Paper elevation={3} sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Category Breakdown
                </Typography>
                <Box sx={{ overflow: "auto" }}>
                  <table style={{ width: "100%", borderCollapse: "collapse" }}>
                    <thead>
                      <tr>
                        <th
                          style={{
                            textAlign: "left",
                            padding: "12px 8px",
                            borderBottom: "1px solid #ddd",
                          }}
                        >
                          Category
                        </th>
                        <th
                          style={{
                            textAlign: "right",
                            padding: "12px 8px",
                            borderBottom: "1px solid #ddd",
                          }}
                        >
                          Revenue
                        </th>
                        <th
                          style={{
                            textAlign: "right",
                            padding: "12px 8px",
                            borderBottom: "1px solid #ddd",
                          }}
                        >
                          % of Total
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {metrics.revenue_by_category.map((category) => (
                        <tr key={category.category_id}>
                          <td
                            style={{
                              padding: "10px 8px",
                              borderBottom: "1px solid #eee",
                            }}
                          >
                            {category.category_name}
                          </td>
                          <td
                            style={{
                              textAlign: "right",
                              padding: "10px 8px",
                              borderBottom: "1px solid #eee",
                            }}
                          >
                            {`R$ ${category.revenue.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
                          </td>
                          <td
                            style={{
                              textAlign: "right",
                              padding: "10px 8px",
                              borderBottom: "1px solid #eee",
                            }}
                          >
                            {`${((category.revenue / metrics.total_revenue) * 100).toFixed(1)}%`}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </Box>
              </Paper>
            </Grid>
          </Grid>
        </>
      ) : null}
    </Container>
  );
}
