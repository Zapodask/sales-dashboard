import { Api } from ".";
import {
  CreateProductProps,
  Product,
  UpdateProductProps,
} from "../../interfaces/product";

export class ProductsApi extends Api {
  constructor() {
    super("/products");
  }

  async createProduct(
    product: CreateProductProps,
    file: File,
  ): Promise<Product> {
    const formData = new FormData();
    formData.append("image", file);
    formData.append("name", product.name);
    formData.append("description", product.description);
    formData.append("price", product.price.toString());
    formData.append("category_ids", JSON.stringify(product.category_ids));

    const { data } = await this.api.post<Product>("", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return data;
  }

  async getProducts(): Promise<Array<Product>> {
    const { data } = await this.api.get<Array<Product>>("");

    return data;
  }

  async getProduct(id: string): Promise<Product> {
    const { data } = await this.api.get<Product>(`/${id}`);

    return data;
  }

  async updateProduct(
    id: string,
    product: UpdateProductProps,
    file?: File,
  ): Promise<Product> {
    const formData = new FormData();
    if (file) formData.append("image", file);
    if (product.name) formData.append("name", product.name);
    if (product.description)
      formData.append("description", product.description);
    if (product.price) formData.append("price", product.price.toString());
    if (product.category_ids)
      formData.append("category_ids", JSON.stringify(product.category_ids));

    const { data } = await this.api.patch<Product>(`/${id}`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return data;
  }

  async deleteProduct(id: string): Promise<void> {
    await this.api.delete(`/${id}`);
  }
}

export const productsApi = new ProductsApi();
