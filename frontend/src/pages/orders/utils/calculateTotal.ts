import { Product } from "../../../interfaces/product";

export const calculateTotal = (
  products: Array<Product>,
  selectedProductIds: Array<string>,
): number => {
  let total = 0;
  let products_to_find = selectedProductIds.length;

  for (const product of products) {
    if (!selectedProductIds.includes(product.id)) {
      continue;
    }

    total += product.price;

    products_to_find -= 1;

    if (products_to_find == 0) {
      break;
    }
  }

  return Number(total.toFixed(2));
};
