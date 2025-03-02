export interface OrdersByPeriod {
  [date: string]: {
    count: number;
    revenue: number;
  };
}

export interface TopProduct {
  product_id: string;
  product_name: string;
  count: number;
}

export interface CategoryRevenue {
  category_id: string;
  category_name: string;
  revenue: number;
}

export interface DashboardMetrics {
  total_orders: number;
  average_order_value: number;
  total_revenue: number;
  orders_by_period: OrdersByPeriod;
  top_products: TopProduct[];
  revenue_by_category: CategoryRevenue[];
}
