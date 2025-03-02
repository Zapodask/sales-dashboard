import { Api } from ".";
import {
  Order,
  CreateOrderProps,
  UpdateOrderProps,
} from "../../interfaces/order";

export class OrdersApi extends Api {
  constructor() {
    super("/orders");
  }

  async createOrder(order: CreateOrderProps): Promise<Order> {
    const { data } = await this.api.post<Order>("", order);

    return data;
  }

  async getOrders(): Promise<Array<Order>> {
    const { data } = await this.api.get<Array<Order>>("");

    return data;
  }

  async getOrder(id: string): Promise<Order> {
    const { data } = await this.api.get<Order>(`/${id}`);

    return data;
  }

  async updateOrder(id: string, order: UpdateOrderProps): Promise<Order> {
    const { data } = await this.api.patch<Order>(`/${id}`, order);

    return data;
  }

  async deleteOrder(id: string): Promise<void> {
    await this.api.delete(`/${id}`);
  }
}

export const ordersApi = new OrdersApi();
