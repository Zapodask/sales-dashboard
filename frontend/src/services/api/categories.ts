import { Api } from ".";
import {
  Category,
  CreateCategoryProps,
  UpdateCategoryProps,
} from "../../interfaces/category";

export class CategoriesApi extends Api {
  constructor() {
    super("/categories");
  }

  async createCategory(category: CreateCategoryProps): Promise<Category> {
    const { data } = await this.api.post<Category>("", category);

    return data;
  }

  async getCategories(): Promise<Array<Category>> {
    const { data } = await this.api.get<Array<Category>>("");

    return data;
  }

  async getCategory(id: string): Promise<Category> {
    const { data } = await this.api.get<Category>(`/${id}`);

    return data;
  }

  async updateCategory(
    id: string,
    category: UpdateCategoryProps,
  ): Promise<Category> {
    const { data } = await this.api.patch<Category>(`/${id}`, category);

    return data;
  }

  async deleteCategory(id: string): Promise<void> {
    await this.api.delete(`/${id}`);
  }
}

export const categoriesApi = new CategoriesApi();
