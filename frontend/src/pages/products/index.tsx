import { useCallback, useEffect, useState } from "react";
import { Box } from "@mui/material";
import { GridColDef } from "@mui/x-data-grid";

import Cell from "../../components/cell";
import DataTable from "../../components/dataTable";
import { Button } from "../../stories/Button";

import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

import { productsApi } from "../../services/api/products";
import { categoriesApi } from "../../services/api/categories";
import { Category } from "../../interfaces/category";
import CreateProductModal from "./components/createProductModal";
import UpdateProductModal from "./components/updateProductModal";

export default function ProductsPage() {
  const [categories, setCategories] = useState<Array<Category>>([]);

  const getColumns = useCallback(
    (
      openUpdateModal: (id: string) => void,
      onRemoveItem: (id: string) => void,
    ): Array<GridColDef> => [
      {
        field: "id",
        headerName: "ID",
        width: 200,
        renderCell: (params) => <Cell value={params.value} />,
      },
      {
        field: "name",
        headerName: "Name",
        width: 200,
        renderCell: (params) => <Cell value={params.value} />,
      },
      {
        field: "description",
        headerName: "Description",
        width: 250,
        renderCell: (params) => <Cell value={params.value} />,
      },
      {
        field: "price",
        headerName: "Price",
        width: 150,
        renderCell: (params) => <Cell value={`R$ ${params.value}`} />,
      },
      {
        field: "actions",
        headerName: "Actions",
        width: 200,
        renderCell: (params) => (
          <Box
            display={"flex"}
            alignItems={"center"}
            width={"100%"}
            height={"100%"}
          >
            <Button
              label="Edit"
              color="primary"
              size="small"
              onClick={(event) => {
                event.stopPropagation();
                openUpdateModal(params.row.id);
              }}
              sx={{ marginRight: 1 }}
              startIcon={<EditIcon />}
            />

            <Button
              label="Delete"
              color="error"
              size="small"
              onClick={(event) => {
                event.stopPropagation();
                const isConfirmed = window.confirm(
                  "Do you really want to remove this product?",
                );
                if (isConfirmed) {
                  const id = params.row.id;
                  productsApi.deleteProduct(id);
                  onRemoveItem(id);
                }
              }}
              startIcon={<DeleteIcon />}
            />
          </Box>
        ),
      },
    ],
    [],
  );

  const getProducts = useCallback(() => productsApi.getProducts(), []);

  useEffect(() => {
    categoriesApi.getCategories().then((data) => setCategories(data));
  }, []);

  return (
    <DataTable
      label="Product"
      getColumns={getColumns}
      getData={getProducts}
      CreateModal={(props) => CreateProductModal({ ...props, categories })}
      UpdateModal={(props) => UpdateProductModal({ ...props, categories })}
    />
  );
}
