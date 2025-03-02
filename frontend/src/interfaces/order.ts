export interface Order {
  id: string;
  date: Date;
  total: number;
  product_ids: string[];
}

export type CreateOrderProps = Omit<Order, "id" | "total">;

export type UpdateOrderProps = Partial<CreateOrderProps>;
