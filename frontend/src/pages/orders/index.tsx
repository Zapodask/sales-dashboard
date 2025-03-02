import { useCallback, useEffect, useState } from "react";
import { GridColDef } from "@mui/x-data-grid";
import { Box } from "@mui/material";
import { format } from "date-fns";

import Cell from "../../components/cell";
import DataTable from "../../components/dataTable";
import { Button } from "../../stories/Button";

import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

import { ordersApi } from "../../services/api/orders";
import { productsApi } from "../../services/api/products";

import { Product } from "../../interfaces/product";

import CreateOrderModal from "./components/createOrderModal";
import UpdateOrderModal from "./components/updateOrderModal";

export default function OrdersPage() {
  const [products, setProducts] = useState<Array<Product>>([]);

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
        field: "total",
        headerName: "Total",
        width: 200,
        renderCell: (params) => <Cell value={`R$ ${params.value}`} />,
      },
      {
        field: "date",
        headerName: "Date",
        width: 100,
        renderCell: (params) => (
          <Cell value={format(params.value, "dd/MM/yyyy")} />
        ),
      },
      {
        field: "actions",
        headerName: "actions",
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
                  "Do you really want to remove this order?",
                );
                if (isConfirmed) {
                  const id = params.row.id;
                  ordersApi.deleteOrder(id);
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

  const getOrders = useCallback(() => ordersApi.getOrders(), []);

  useEffect(() => {
    productsApi.getProducts().then((data) => setProducts(data));
  }, []);

  return (
    <DataTable
      label="Order"
      getColumns={getColumns}
      getData={getOrders}
      CreateModal={(props) => CreateOrderModal({ ...props, products })}
      UpdateModal={(props) => UpdateOrderModal({ ...props, products })}
    />
  );
}
