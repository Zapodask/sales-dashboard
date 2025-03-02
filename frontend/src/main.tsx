import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFnsV3";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { ptBR } from "date-fns/locale";

import DashboardPage from "./pages/dashboard/index.tsx";
import ProductsPage from "./pages/products/index.tsx";
import CategoriesPage from "./pages/categories/index.tsx";
import OrdersPage from "./pages/orders/index.tsx";

import App from "./app.tsx";
import Layout from "./layout.tsx";

const router = createBrowserRouter([
  {
    Component: App,
    children: [
      {
        path: "/",
        Component: Layout,
        children: [
          {
            path: "/",
            Component: DashboardPage,
          },
          {
            path: "/products",
            Component: ProductsPage,
          },
          {
            path: "/categories",
            Component: CategoriesPage,
          },
          {
            path: "/orders",
            Component: OrdersPage,
          },
        ],
      },
    ],
  },
]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ptBR}>
      <RouterProvider router={router} />
    </LocalizationProvider>
  </StrictMode>,
);
