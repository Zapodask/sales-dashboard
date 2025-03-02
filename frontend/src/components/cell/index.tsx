import { Box, Tooltip, Typography } from "@mui/material";

export default function Cell({ value }: { value: any }) {
  return (
    <Tooltip title={value} arrow>
      <Box
        display={"flex"}
        alignItems={"center"}
        width={"100%"}
        height={"100%"}
      >
        <Typography noWrap>{value}</Typography>
      </Box>
    </Tooltip>
  );
}
