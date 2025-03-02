import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  Button,
  Box,
} from "@mui/material";
import { useForm } from "react-hook-form";
import { Category } from "../../../../interfaces/category";
import { UpdateModalProps } from "../../../../components/dataTable";
import { categoriesApi } from "../../../../services/api/categories";

interface CategoryFormValues {
  name: string;
}

export default function UpdateCategoryModal({
  open,
  item,
  onClose,
  onSubmit,
}: UpdateModalProps<Category>) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CategoryFormValues>({
    defaultValues: {
      name: item.name,
    },
  });

  const handleFormSubmit = async (data: CategoryFormValues) => {
    try {
      const category = await categoriesApi.updateCategory(item.id, {
        name: data.name,
      });

      onSubmit(category);
      onClose();
      reset();
    } catch (error) {
      console.error("Error updating category:", error);
      onSubmit(null);
    }
  };

  const onCancel = () => {
    onClose();
    reset();
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle sx={{ fontWeight: "bold" }}>Update category</DialogTitle>
      <DialogContent>
        <Box
          component="form"
          onSubmit={handleSubmit(handleFormSubmit)}
          sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}
        >
          <TextField
            {...register("name", { required: "Name is required" })}
            label="Name"
            variant="outlined"
            fullWidth
            error={!!errors.name}
            helperText={errors.name?.message}
          />
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
