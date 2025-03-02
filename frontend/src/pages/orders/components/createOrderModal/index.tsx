import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Button,
  MenuItem,
  InputLabel,
  FormControl,
  Select,
  Chip,
  Box,
} from "@mui/material";
import { useForm, Controller } from "react-hook-form";
import { DatePicker } from "@mui/x-date-pickers";
import { CreateModalProps } from "../../../../components/dataTable";
import { Order } from "../../../../interfaces/order";
import { Product } from "../../../../interfaces/product";
import { ordersApi } from "../../../../services/api/orders";
import { calculateTotal } from "../../utils/calculateTotal";
import { useMemo } from "react";

interface OrderFormValues {
  date: Date;
  productIds: string[];
}

interface CreateOrderModalProps extends CreateModalProps<Order> {
  products: Array<Product>;
}

export default function CreateOrderModal({
  open,
  products,
  onClose,
  onSubmit,
}: CreateOrderModalProps) {
  const {
    handleSubmit,
    formState: { errors },
    control,
    reset,
    watch,
  } = useForm<OrderFormValues>({
    defaultValues: {
      productIds: [],
      date: new Date(),
    },
  });

  const selectedProductIds = watch("productIds");

  const total = useMemo(() => {
    return calculateTotal(products, selectedProductIds);
  }, [products, selectedProductIds]);

  const handleFormSubmit = async (data: OrderFormValues) => {
    try {
      const order = await ordersApi.createOrder({
        date: data.date,
        product_ids: data.productIds,
      });

      onSubmit(order);
      onClose();
      reset();
    } catch (error) {
      console.error("Error creating order:", error);
      onSubmit(null);
    }
  };

  const onCancel = () => {
    reset();
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle sx={{ fontWeight: "bold" }}>Create Order</DialogTitle>
      <DialogContent>
        <Box
          component="form"
          onSubmit={handleSubmit(handleFormSubmit)}
          sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}
        >
          <Controller
            name="date"
            control={control}
            render={({ field }) => (
              <DatePicker {...field} label="Date" format="dd/MM/yyyy" />
            )}
          />

          <FormControl fullWidth error={!!errors.productIds}>
            <InputLabel>Produtos</InputLabel>
            <Controller
              name="productIds"
              control={control}
              rules={{ required: "Products are required" }}
              render={({ field }) => (
                <Select
                  {...field}
                  multiple
                  onChange={(event) => field.onChange(event.target.value)}
                  renderValue={(selected) => (
                    <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
                      {(selected as string[]).map((value) => {
                        const product = products.find((p) => p.id === value);
                        return product ? (
                          <Chip key={value} label={product.name} />
                        ) : null;
                      })}
                    </Box>
                  )}
                >
                  {products.map((product) => (
                    <MenuItem key={product.id} value={product.id}>
                      {product.name}
                    </MenuItem>
                  ))}
                </Select>
              )}
            />
            {errors.productIds && (
              <Box sx={{ color: "error.main", fontSize: "0.875rem", mt: 0.5 }}>
                {errors.productIds.message}
              </Box>
            )}
          </FormControl>

          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              fontWeight: "bold",
            }}
          >
            <p>Total: R$ {total}</p>
          </Box>
        </Box>
      </DialogContent>
      <DialogActions sx={{ p: 2 }}>
        <Button onClick={onCancel} color="inherit" variant="outlined">
          Close
        </Button>
        <Button
          onClick={handleSubmit(handleFormSubmit)}
          color="primary"
          variant="contained"
        >
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
}
