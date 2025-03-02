import { Meta, StoryObj } from "@storybook/react";
import { DataGrid } from "./DataGrid";
import { DataGridProps, GridColDef } from "@mui/x-data-grid";

const meta: Meta<typeof DataGrid> = {
  title: "Components/DataGrid",
  component: DataGrid,
  argTypes: {
    rows: { control: "object" },
    columns: { control: "object" },
  },
};

export default meta;

const mockColumns: GridColDef[] = [
  { field: "id", headerName: "ID", width: 100 },
  { field: "name", headerName: "Name", width: 100 },
  { field: "description", headerName: "description", width: 250 },
];

const mockRows = [
  { id: 1, name: "Ball", description: "Soccer ball" },
  { id: 2, name: "Chair", description: "Wooden chair" },
  {
    id: 3,
    name: "Table",
    description: "Wooden table",
  },
];

export const Default: StoryObj<DataGridProps> = {
  args: {
    rows: mockRows,
    columns: mockColumns,
    autoHeight: true,
    pageSizeOptions: [5, 10, 15],
  },
};

export const WithPagination: StoryObj<DataGridProps> = {
  args: {
    rows: mockRows,
    columns: mockColumns,
    autoHeight: true,
    pageSizeOptions: [5, 10, 15],
    pagination: true,
  },
};
