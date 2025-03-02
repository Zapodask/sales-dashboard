import { useCallback } from "react";
import { GridColDef } from "@mui/x-data-grid";
import { Box } from "@mui/material";

import Cell from "../../components/cell";
import DataTable from "../../components/dataTable";
import { Button } from "../../stories/Button";

import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

import { categoriesApi } from "../../services/api/categories";
import CreateCategoryModal from "./components/createCategoryModal";
import UpdateCategoryModal from "./components/updateCategoryModal";

export default function CategoriesPage() {
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
              onClick={async (event) => {
                event.stopPropagation();
                const isConfirmed = window.confirm(
                  "Do you really want to remove this category?",
                );
                if (isConfirmed) {
                  const id = params.row.id;
                  categoriesApi.deleteCategory(id);

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

  const getCategories = useCallback(() => categoriesApi.getCategories(), []);

  return (
    <DataTable
      label="Category"
      getColumns={getColumns}
      getData={getCategories}
      CreateModal={CreateCategoryModal}
      UpdateModal={UpdateCategoryModal}
    />
  );
}
