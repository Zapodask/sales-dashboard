import { useCallback, useEffect, useState } from "react";

import { Box, Fade, Snackbar } from "@mui/material";
import { GridColDef, GridPaginationModel } from "@mui/x-data-grid";
import { TransitionProps } from "@mui/material/transitions";

import AddIcon from "@mui/icons-material/Add";

import { IconButton } from "../../stories/IconButton";
import { DataGrid } from "../../stories/DataGrid";

import { Product } from "../../interfaces/product";
import { Category } from "../../interfaces/category";
import { Order } from "../../interfaces/order";

type AllowedDataTypes = Product | Category | Order;

type Label = "Category" | "Order" | "Product";

export interface ModalProps<TData extends AllowedDataTypes> {
  open: boolean;
  onClose: () => void;
  onSubmit: (item: TData | null) => void;
}

export type CreateModalProps<TData extends AllowedDataTypes> =
  ModalProps<TData>;

export interface UpdateModalProps<TData extends AllowedDataTypes>
  extends ModalProps<TData> {
  item: TData;
}

interface DataTableProps<TData extends AllowedDataTypes> {
  label: Label;
  getColumns: (
    openUpdateModal: (id: string) => void,
    onRemoveItem: (id: string) => void,
  ) => Array<GridColDef>;
  getData: () => Promise<Array<TData>>;
  CreateModal: React.ComponentType<CreateModalProps<TData>>;
  UpdateModal: React.ComponentType<UpdateModalProps<TData>>;
}

export default function DataTable<TData extends AllowedDataTypes>(
  props: DataTableProps<TData>,
) {
  const { CreateModal, UpdateModal } = props;
  const [data, setData] = useState<Array<TData>>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [paginationModel, setPaginationModel] = useState<GridPaginationModel>({
    page: 0,
    pageSize: 10,
  });

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showUpdateModal, setShowUpdateModal] = useState(false);
  const [itemToUpdate, setItemToUpdate] = useState<TData | null>(null);

  const [snackbarState, setSnackbarState] = useState<{
    open: boolean;
    Transition: React.ComponentType<
      TransitionProps & {
        children: React.ReactElement<any, any>;
      }
    >;
    message: string;
  }>({
    open: false,
    Transition: Fade,
    message: "",
  });

  const closeSnackbar = () => {
    setSnackbarState({ ...snackbarState, open: false });
  };

  const handleChangePaginationModel = (value: GridPaginationModel) => {
    setPaginationModel(value);
  };

  const handleChangeCreateModal = () => {
    setShowCreateModal(!showCreateModal);
  };

  const handleChangeUpdateModal = useCallback(() => {
    if (showUpdateModal) setItemToUpdate(null);
    setShowUpdateModal(!showUpdateModal);
  }, [showUpdateModal]);

  const getData = async () => {
    setIsLoading(true);
    try {
      setData(await props.getData());
    } catch (error) {
      console.log(error);
      setSnackbarState({
        open: true,
        Transition: Fade,
        message: "Error getting data",
      });
    }
    setIsLoading(false);
  };

  const openUpdateModal = useCallback(
    (id: string) => {
      const item = data.find((item) => item.id === id);
      if (item) {
        setItemToUpdate(item);
        handleChangeUpdateModal();
      }
    },
    [data, handleChangeUpdateModal],
  );

  const onRemoveItem = useCallback((id: string) => {
    setData((prevData) => prevData.filter((item) => item.id.toString() !== id));
  }, []);

  const onCreateItem = useCallback(
    (item: TData | null) => {
      if (item === null) {
        setSnackbarState({
          open: true,
          Transition: Fade,
          message: `Error creating ${props.label.toLowerCase()}`,
        });
        return;
      }

      setData((prevData) => [...prevData, item]);

      setSnackbarState({
        open: true,
        Transition: Fade,
        message: `${props.label} created successfully`,
      });
    },
    [props.label],
  );

  const onUpdateItem = useCallback(
    (item: TData | null) => {
      if (item === null) {
        setSnackbarState({
          open: true,
          Transition: Fade,
          message: `Error updating ${props.label.toLowerCase()}`,
        });
        return;
      }

      setData((prevData) => {
        const item_index = prevData.findIndex(
          (prevItem) => prevItem.id === item.id,
        );
        const newData = [...prevData];

        newData[item_index] = item;

        return newData;
      });

      setSnackbarState({
        open: true,
        Transition: Fade,
        message: `${props.label} updated successfully`,
      });
    },
    [props.label],
  );

  useEffect(() => {
    getData();
  }, []);

  return (
    <div>
      <Box display={"flex"} justifyContent={"end"} mb={2}>
        <IconButton onClick={handleChangeCreateModal} loading={isLoading}>
          <AddIcon />
        </IconButton>
      </Box>

      <DataGrid
        rows={data}
        getRowId={(row: TData) => row.id}
        columns={props.getColumns(openUpdateModal, onRemoveItem)}
        pagination={true}
        paginationModel={paginationModel}
        onPaginationModelChange={handleChangePaginationModel}
        pageSizeOptions={[10, 25, 50, 100]}
        loading={isLoading}
        checkboxSelection
        sx={{ border: 0 }}
      />

      <CreateModal
        open={showCreateModal}
        onSubmit={onCreateItem}
        onClose={handleChangeCreateModal}
      />

      {itemToUpdate && (
        <UpdateModal
          open={showUpdateModal}
          item={itemToUpdate}
          onSubmit={onUpdateItem}
          onClose={handleChangeUpdateModal}
        />
      )}

      <Snackbar
        open={snackbarState.open}
        slots={{ transition: snackbarState.Transition }}
        message={snackbarState.message}
        key={snackbarState.Transition.name}
        autoHideDuration={1000}
        onClose={closeSnackbar}
      />
    </div>
  );
}
