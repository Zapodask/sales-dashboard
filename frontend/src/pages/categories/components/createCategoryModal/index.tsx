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
import { categoriesApi } from "../../../../services/api/categories";
import { CreateModalProps } from "../../../../components/dataTable";
import { Category } from "../../../../interfaces/category";

interface CategoryFormValues {
  name: string;
}

export default function CreateCategoryModal({
  open,
  onClose,
  onSubmit,
}: CreateModalProps<Category>) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm({
    defaultValues: {
      name: "",
    },
  });

  const handleFormSubmit = async (data: CategoryFormValues) => {
    try {
      const category = await categoriesApi.createCategory({
        name: data.name,
      });

      onSubmit(category);
      onClose();
      reset();
    } catch (error) {
      console.error("Error creating category:", error);
      onSubmit(null);
    }
  };

  const onCancel = () => {
    onClose();
    reset();
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle sx={{ fontWeight: "bold" }}>Create category</DialogTitle>
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
