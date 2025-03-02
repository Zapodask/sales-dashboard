export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  category_ids: string[];
  image_url: string;
}

export type CreateProductProps = Omit<Product, "id" | "image_url">;

export type UpdateProductProps = Partial<CreateProductProps>;
