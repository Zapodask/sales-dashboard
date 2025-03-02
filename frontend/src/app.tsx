import { type Navigation } from "@toolpad/core/AppProvider";

import { Outlet } from "react-router";
import { ReactRouterAppProvider } from "@toolpad/core/react-router";

import CategoryIcon from "@mui/icons-material/Category";
import ChairIcon from "@mui/icons-material/Chair";
import DashboardIcon from "@mui/icons-material/Dashboard";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";

const NAVIGATION: Navigation = [
  {
    title: "Dashboard",
    icon: <DashboardIcon />,
  },
  {
    segment: "products",
    title: "Products",
    icon: <ChairIcon />,
  },
  {
    segment: "categories",
    title: "Categories",
    icon: <CategoryIcon />,
  },
  {
    segment: "orders",
    title: "Orders",
    icon: <ShoppingCartIcon />,
  },
];

export default function App() {
  return (
    <ReactRouterAppProvider
      navigation={NAVIGATION}
      branding={{
        title: "Sales dachboard",
      }}
    >
      <Outlet />
    </ReactRouterAppProvider>
  );
}
