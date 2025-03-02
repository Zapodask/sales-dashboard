import { useState } from "react";
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  Button,
  MenuItem,
  InputLabel,
  FormControl,
  Select,
  Chip,
  Box,
} from "@mui/material";
import { useForm, Controller } from "react-hook-form";
import { NumericFormat } from "react-number-format";
import { useDropzone } from "react-dropzone";
import { CreateModalProps } from "../../../../components/dataTable";
import { Product } from "../../../../interfaces/product";
import { Category } from "../../../../interfaces/category";
import { productsApi } from "../../../../services/api/products";

interface ProductFormValues {
  name: string;
  description: string;
  price: string;
  categoryIds: string[];
  image: File | null;
}

interface CreateProductModalProps extends CreateModalProps<Product> {
  categories: Array<Category>;
}

export default function CreateProductModal({
  open,
  categories,
  onClose,
  onSubmit,
}: CreateProductModalProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    control,
    reset,
    setValue,
  } = useForm({
    defaultValues: {
      categoryIds: [],
      name: "",
      description: "",
      price: "",
      image: null,
    },
  });

  const [imagePreview, setImagePreview] = useState<string | null>(null);

  const onDrop = (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    setValue("image", file as any);
    setImagePreview(URL.createObjectURL(file));
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
      "image/*": [],
    },
    multiple: false,
  });

  const handleFormSubmit = async (data: ProductFormValues) => {
    if (!data.image) return;

    const formattedPrice = Number(
      data.price.replace("R$", "").replace(",", ".").trim(),
    );

    try {
      const product = await productsApi.createProduct(
        {
          name: data.name,
          description: data.description,
          price: formattedPrice,
          category_ids: data.categoryIds,
        },
        data.image,
      );

      onSubmit(product);
      onClose();
      reset();
      setImagePreview(null);
    } catch (error) {
      console.error("Error creating product:", error);
      onSubmit(null);
    }
  };

  const onCancel = () => {
    reset();
    setImagePreview(null);
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle sx={{ fontWeight: "bold" }}>Create product</DialogTitle>
      <DialogContent>
        <Box
          component="form"
          onSubmit={handleSubmit(handleFormSubmit)}
          sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}
        >
          <Box
            {...getRootProps()}
            sx={{
              border: "2px dashed #ccc",
              padding: 2,
              textAlign: "center",
              cursor: "pointer",
              borderRadius: 1,
              backgroundColor: "#f5f5f5",
            }}
          >
            <input {...getInputProps()} />
            {imagePreview ? (
              <img
                src={imagePreview}
                alt="preview"
                style={{ width: "100%", height: "auto" }}
              />
            ) : (
              <p>Drag 'n' drop an image here, or click to select an image</p>
            )}
          </Box>
          <TextField
            {...register("name", { required: "Name is required" })}
            label="Name"
            variant="outlined"
            fullWidth
            error={!!errors.name}
            helperText={errors.name?.message}
          />
          <TextField
            {...register("description", {
              required: "Description is required",
            })}
            label="Description"
            variant="outlined"
            fullWidth
            multiline
            rows={3}
            error={!!errors.description}
            helperText={errors.description?.message}
          />

          <Controller
            name="price"
            control={control}
            rules={{ required: "Price is required" }}
            render={({ field }) => (
              <NumericFormat
                {...field}
                customInput={TextField}
                label="Price"
                variant="outlined"
                fullWidth
                decimalSeparator=","
                thousandSeparator="."
                prefix="R$ "
                allowNegative={false}
                error={!!errors.price}
                helperText={errors.price?.message}
                onValueChange={(values) => {
                  field.onChange(values.value);
                }}
              />
            )}
          />

          <FormControl fullWidth error={!!errors.categoryIds}>
            <InputLabel>Categories</InputLabel>
            <Controller
              name="categoryIds"
              control={control}
              render={({ field }) => (
                <Select
                  {...field}
                  multiple
                  onChange={(event) => field.onChange(event.target.value)}
                  renderValue={(selected) => (
                    <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
                      {(selected as string[]).map((value) => {
                        const category = categories.find((c) => c.id === value);
                        return category ? (
                          <Chip key={value} label={category.name} />
                        ) : null;
                      })}
                    </Box>
                  )}
                >
                  {categories.map((category) => (
                    <MenuItem key={category.id} value={category.id}>
                      {category.name}
                    </MenuItem>
                  ))}
                </Select>
              )}
            />
            {errors.categoryIds && (
              <Box sx={{ color: "error.main", fontSize: "0.875rem", mt: 0.5 }}>
                {errors.categoryIds.message}
              </Box>
            )}
          </FormControl>
        </Box>
      </DialogContent>
      <DialogActions sx={{ p: 2 }}>
        <Button onClick={onCancel} color="inherit" variant="outlined">
          close
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
