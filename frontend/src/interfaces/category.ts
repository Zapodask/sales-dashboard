export interface Category {
  id: string;
  name: string;
}

export type CreateCategoryProps = Omit<Category, "id">;

export type UpdateCategoryProps = Partial<CreateCategoryProps>;
